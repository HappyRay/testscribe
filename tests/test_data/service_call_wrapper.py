from test_data.search_person import search_person_age_with_fixed_service
from test_data.service_call import Service
from test_scribe.mocking_support import patch


def search_age_with_patched_service(name: str) -> int:
    patch(target="test_data.service_call.Service", spec=Service)
    return search_person_age_with_fixed_service(name)
