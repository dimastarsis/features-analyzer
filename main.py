import asyncio
import network
import parser
import analyzer
import writer


async def main() -> None:
    network.API.set_session()

    features_v2_file = network.ProjectFile.parse(network.FEATURES_V2_URL)
    config_file = network.ProjectFile.parse(network.CONFIG_URL)

    features_v2_text, config_text = await network.gitlab.fetch_files(features_v2_file, config_file)

    features_v2_flags = parser.features_v2.extract_flags(features_v2_text)
    config_flags = parser.config.extract_flags(config_text)

    print(f"Извлекли из модели v2 {len(features_v2_flags)} флагов")
    print(f"Извлекли из конфига {len(config_flags)} флагов", flush=True)
    await asyncio.sleep(1)

    keadmin_flag_infos = await network.keadmin.fetch_infos(
        map(
            lambda feature_v2_flag: feature_v2_flag.keadmin_search_name,
            features_v2_flags.values()
        )
    )

    analyze_results = analyzer.features_v2.analyze(features_v2_flags, config_flags, keadmin_flag_infos)
    writer.write_csv(analyze_results)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except asyncio.CancelledError:
        pass
    finally:
        loop.run_until_complete(network.API.close())
        loop.close()
