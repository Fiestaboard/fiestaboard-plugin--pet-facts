"""Display a random fun fact about cats or dogs."""

from __future__ import annotations

import logging
from typing import Any, Dict, List
import requests
import random
from src.plugins.base import PluginBase, PluginResult

logger = logging.getLogger(__name__)

API_URL = "https://catfact.ninja/fact"
USER_AGENT = "FiestaBoard Pet Facts Plugin (https://github.com/Fiestaboard/fiestaboard-plugin--pet-facts)"


class PetFactsPlugin(PluginBase):
    """Pet Facts plugin for FiestaBoard."""

    @property
    def plugin_id(self) -> str:
        return "pet_facts"

    def fetch_data(self) -> PluginResult:
        try:
            animal = self.config.get("animal") or "random"
            if animal == "random":
                animal = random.choice(["cat", "dog"])

            if animal == "cat":
                response = requests.get(
                    "https://catfact.ninja/fact",
                    headers={"User-Agent": USER_AGENT},
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()
                fact = str(data.get("fact", ""))[:22]
            else:
                response = requests.get(
                    "https://dogapi.dog/api/v2/facts",
                    headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()
                facts = data.get("data", [])
                if facts:
                    fact = str(facts[0].get("attributes", {}).get("body", ""))[:22]
                else:
                    fact = "Dogs are loyal companions."

            return PluginResult(
                available=True,
                data={
                    "fact": fact,
                    "animal": animal,
                },
            )
        except Exception as e:
            logger.exception("Error fetching pet fact")
            return PluginResult(available=False, error=str(e))

    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        return []

    def cleanup(self) -> None:
        pass
