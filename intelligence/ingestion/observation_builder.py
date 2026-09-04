from ..models.observations import Observation


def build_observations(records, source_reliability=0.5):
    """
    Convert validated intelligence records into
    Observation objects.
    """

    observations = []

    for index, record in enumerate(records, start=1):

        observation = Observation(
            observation_id=f"OBS-{index:03d}",

            source=record["source"],

            content=record["content"],

            observed_at=record.get("observed_at"),

            source_reliability=source_reliability
        )

        observations.append(observation)

    return observations