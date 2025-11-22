from src.shared.dependencies.container import Container
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered

from src.llm.application.use_cases.rows_to_cards import RowsToCards
from   src.llm.application.agents.generate_bio import GernerateBio

from src.llm.dependencies.agents import get_card_parser_agent, get_bio_generator_agent
from src.shared.dependencies.services import get_ws_transport

def get_rows_to_cards_use_case() -> RowsToCards:
    try:
        instance_key = "csv_to_card_use_case"
        use_case = Container.resolve(instance_key)
    except DependencyNotRegistered:
        agent = get_card_parser_agent()
        ws_transport = get_ws_transport()
        use_case = RowsToCards(
            smart_card_parser=agent,
            ws_transport=ws_transport
        )
        Container.register(instance_key, use_case)

    return use_case


def get_generate_bio_use_case() -> GernerateBio:
    try:
        instance_key = "generate_bio_use_case"
        use_case = Container.resolve(instance_key)
    except DependencyNotRegistered:
        agent = get_bio_generator_agent()
        use_case = GernerateBio(
            bio_generator=agent
        )
        Container.register(instance_key, use_case)

    return use_case