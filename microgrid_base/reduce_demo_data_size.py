from log_utils import logger_print

from mock_utils import modifyValueIfNumber, modifyIfIsDeviceCount

if __name__ == "__main__":
    from json_utils import jsonApply
    import json

    with open("test_output_full_mock.json", "r") as f:
        json_obj = json.load(f)

    applied_json_obj = jsonApply(json_obj, modifyValueIfNumber, modifyIfIsDeviceCount)
    output_file = "test_output_full_mock_reduced.json"
    with open(output_file, "w+") as f:
        f.write(json.dumps(applied_json_obj, indent=4, ensure_ascii=False))
