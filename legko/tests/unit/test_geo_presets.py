from legko.domain.geo_presets import GEO_PRESETS, filter_geo_presets


def test_filter_geo_by_code_prefix():
    items = filter_geo_presets("au")
    assert items and items[0]["code"] == "AU"


def test_filter_geo_by_name():
    items = filter_geo_presets("перу")
    assert any(row["code"] == "PE" for row in items)


def test_preset_list_not_empty():
    assert len(GEO_PRESETS) >= 40