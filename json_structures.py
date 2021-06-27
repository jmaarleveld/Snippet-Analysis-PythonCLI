import json_util


JSON_STRUCTURE = json_util.Object(
    nonterminals=json_util.Dict(json_util.Number(),
                                json_util.String()),
    results=json_util.Dict(json_util.Tuple(json_util.String(),
                                           json_util.String(),
                                           json_util.Number()),
                           json_util.Object(
                               classification=json_util.Number(),
                               source=json_util.String(),
                               stripped_comments=json_util.Bool(),
                               is_custom=json_util.Bool(),
                               uses_custom=json_util.Bool(),
                               old_file=json_util.String(),
                               new_file=json_util.String(),
                               adjusted_source=json_util.String()
                           )),
    order=json_util.List(json_util.Tuple(json_util.String(),
                                         json_util.String(),
                                         json_util.Number())
                         ),
    meaningful_threshold=json_util.Number()
)

BENCH_JSON_STRUCTURE = json_util.List(
    json_util.Object(
        old_hash=json_util.String(),
        new_hash=json_util.String(),
        diffs=json_util.List(
            json_util.Object(
                old_file=json_util.String(),
                new_file=json_util.String(),
                old_file_benchmark=json_util.Object(
                    success=json_util.Bool(),
                    times=json_util.List(json_util.Number()),
                    ambiguities=json_util.Number()
                ),
                new_file_benchmark=json_util.Object(
                    success=json_util.Bool(),
                    times=json_util.List(json_util.Number()),
                    ambiguities=json_util.Number()
                ),
                snippets=json_util.List(
                    json_util.Object(
                        snippet_key=json_util.Tuple(
                            json_util.String(),
                            json_util.String(),
                            json_util.Number()
                        ),
                        benchmark=json_util.Object(
                            allow_empty=True,
                            success=json_util.Bool(),
                            times=json_util.List(
                                json_util.Number()
                            ),
                            ambiguities=json_util.Number()
                        )
                    )
                )
            )
        )
    )
)