import egglog.bindings as egglog


def exec_cmd(cmd):
    match cmd:
        case egglog.RuleCommand(name, ruleset, egglog.Rule(span, head, body)):
            pass
        case egglog.Function(
            egglog.FunctionDecl(
                name,
                schema,
                default,
                merge,
                merge_action,
                cost,
                unextractable,
                ignore_viz,
            )
        ):
            pass
        case egglog.RewriteCommand(
            name, egglog.Rewrite(conditions, lhs, rhs, span), subsume
        ):
            pass
        case egglog.Run(egglog.RunConfig(ruleset, until), span):
            pass
        case _:
            raise NotImplementedError(cmd)


def run(prog: str, egraph):
    cmds = egglog.parse_program(prog)
    for cmd in cmds:
        exec_cmd(cmd, egraph)
