import asyncio
import network
import parser
import analyzer
import writer


async def main() -> None:
    network.API.set_session()

    features_v2_file = network.GitLabFileReference.parse(network.FEATURES_V2_URL)
    config_file = network.GitLabFileReference.parse(network.CONFIG_URL)

    features_v2_file, config_file = await network.gitlab.fetch_files(features_v2_file, config_file)

    features_v2_flags = parser.features_v2.extract_flags(features_v2_file.content)
    config_flags = parser.config.extract_flags(config_file.content)

    await asyncio.sleep(0.5)  # чтобы корректно напечаталось

    keadmin_flag_infos = await network.keadmin.fetch_infos(
        map(lambda feature_v2_flag: feature_v2_flag.keadmin_search_name, features_v2_flags.values())
    )
    youtrack_flag_infos = await network.youtrack.fetch_infos(
        {feature_v2_flag_key: features_v2_flags[feature_v2_flag_key].youtrack_search_names
         for feature_v2_flag_key in features_v2_flags}
    )

    analyze_results = analyzer.features_v2.analyze(
        features_v2_flags, config_flags, keadmin_flag_infos, youtrack_flag_infos
    )
    writer.write_csv(analyze_results, features_v2_file, config_file)


if __name__ == "__main__":  # todo тесты, убрать requests из .toml
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except asyncio.CancelledError:
        pass
    finally:
        loop.run_until_complete(network.API.close())
        loop.close()
