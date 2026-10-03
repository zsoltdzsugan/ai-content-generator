from datetime import datetime, UTC
from models.research import Research
from models.source import Source, SourceType
from pipeline.search_process import SearchProcess
from pipeline.evaluator_process import EvaluatorProcess

class ResearchProcess:
    def run(self, query: str, category: str = "", max_attempt: int = 5) -> Research:
        research = Research(query)
        research.start()

        search_process = SearchProcess()
        eval_process = EvaluatorProcess(0.3)

        attempt: int = 0
        sources: list[Source] = []
        exclude_domains: list[str] = []
        while len(sources) < 5 and attempt < max_attempt:
            search_results: list[Source] = search_process.get_sources(query, category, exclude_domains)
            evaluated_sources, exclude_domains = eval_process.evaluate(search_results)
            sources.extend(evaluated_sources)
            attempt += 1
            
        if len(sources) == 0:
            research.fail()
            return research

        research.add_sources(sources)
        research.complete()

        return research
