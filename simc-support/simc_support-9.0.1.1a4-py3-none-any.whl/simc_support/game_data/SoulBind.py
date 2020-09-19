import json
import pkg_resources
import typing


from simc_support.game_data.Language import Translation, _get_translations
from simc_support.game_data.SimcObject import SimcObject
from simc_support.game_data.Covenant import Covenant, get_covenant


class SoulBind(SimcObject):
    """Shadowlands specific additional talent tree."""

    def __init__(
        self,
        *args,
        id: int,
        covenant: Covenant,
        translations: typing.Union[typing.Dict, Translation],
        soul_bind_talents: typing.List["SoulBindTalent"],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.id = id
        self.covenant = covenant
        self.soul_bind_talents = soul_bind_talents

        if isinstance(translations, Translation):
            self.translations = translations
        elif isinstance(translations, dict):
            self.translations = Translation(translations=translations)
        else:
            raise TypeError(
                "translations must either be a dictionary or a Translaton object."
            )


class SoulBindTalent(SimcObject):
    def __init__(
        self,
        *args,
        id: int,
        tier: int,
        order: int,
        parent_id: int,
        type: int,
        translations: typing.Union[typing.Dict, Translation],
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.id = id
        self.tier = tier
        self.order = order
        self.parent_id = parent_id
        self.type = type
        if isinstance(translations, Translation):
            self.translations = translations
        elif isinstance(translations, dict):
            self.translations = Translation(translations=translations)
        else:
            raise TypeError(
                "translations must either be a dictionary or a Translaton object."
            )


def _load_soul_binds() -> typing.List[SoulBind]:
    with pkg_resources.resource_stream(
        __name__, "/".join(("data_files", "soul_binds.json"))
    ) as f:
        loaded_soul_binds = json.load(f)

    def create_talent(dict) -> SoulBindTalent:
        return SoulBindTalent(
            id=dict["id"],
            tier=dict["tier"],
            order=dict["ui_order"],
            parent_id=dict["id_garr_talent_prereq"],
            type=dict["conduit_type"],
            translations=_get_translations(dict),
            full_name=dict["name"],
            simc_name=dict["name"].lower().replace(" ", "_"),
        )

    soul_binds = []
    for soul_bind in loaded_soul_binds:
        soul_binds.append(
            SoulBind(
                id=soul_bind["id"],
                covenant=get_covenant(id=soul_bind["id_covenant"]),
                translations=_get_translations(soul_bind),
                full_name=soul_bind["name"],
                simc_name=soul_bind["name"].lower().replace(" ", "_"),
                soul_bind_talents=[
                    create_talent(talent) for talent in soul_bind["talents"]
                ],
            )
        )
    return soul_binds


SOULBINDS = _load_soul_binds()


def get_soul_bind(*, id: int = None, name: str = None) -> SoulBind:
    if not id and not name:
        raise ValueError("Function requires either 'id' or 'name'.")

    for soul_bind in SOULBINDS:
        if name and name == soul_bind.full_name or id and id == soul_bind.id:
            return soul_bind
    raise ValueError(f"No Soul Bind with id '{id}' or name '{name}' found.")
