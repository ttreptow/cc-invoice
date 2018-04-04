

class TestFilterService:
    def test_get_active_filters_empty(self, filter_service):
        filters = filter_service.get_active_filters()

        assert [] == filters

    def test_get_active_filters(self, filter_service):
        filter_service.add_filter("campaign_id", "eq", 1)

        active_filters = filter_service.get_active_filters()

        assert 1 == len(active_filters)

    def test_clear_active_filters(self, filter_service):
        filter_service.add_filter("campaign_id", "eq", 1)

        filter_service.clear_active_filters()

        assert 0 == len(filter_service.get_active_filters())

    def test_set_get_filter_preserves_value_type(self, filter_service):
        filter_service.add_filter("campaign_id", "eq", 1)

        active_filters = filter_service.get_active_filters()

        assert 1 == active_filters[0].values

    def test_set_get_filter_with_list_values(self, filter_service):
        filter_service.add_filter("campaign_id", "in", [1, 2, 3])

        active_filters = filter_service.get_active_filters()

        assert [1, 2, 3] == active_filters[0].values
