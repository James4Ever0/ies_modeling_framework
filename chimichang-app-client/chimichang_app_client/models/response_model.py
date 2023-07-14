from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ResponseModel")


@attr.s(auto_attribs=True)
class ResponseModel:
    """model summary or description? example response model

    Example:
        {'ans': 'Foo', 'ans_1': 'ans_1 data'}

    Attributes:
        ans (str): pydantic description Example: ans example.
        ans_1 (str):
    """

    ans: str
    ans_1: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        ans = self.ans
        ans_1 = self.ans_1

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ans": ans,
                "ans_1": ans_1,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ans = d.pop("ans")

        ans_1 = d.pop("ans_1")

        response_model = cls(
            ans=ans,
            ans_1=ans_1,
        )

        response_model.additional_properties = d
        return response_model

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
