from trophic.ioi import TEMPLATES


def test_prompt_structure(prompts):
    ioi, abc = prompts
    assert len(ioi) == len(abc) == 2 * len(TEMPLATES)
    for p, q in zip(ioi, abc):
        words = p.text.replace(",", " ").replace(".", " ").split()
        assert words.count(p.s.strip()) == 2          # S appears twice
        assert words.count(p.io.strip()) == 1         # IO once, and it is the answer
        assert p.io != p.s
        assert p.template == q.template and p.place == q.place and p.obj == q.obj
        qwords = q.text.replace(",", " ").replace(".", " ").split()
        assert len(set(q.names)) == 3                  # ABC: three distinct names, none repeated
        assert not {p.io.strip(), p.s.strip()} & set(q.names)
        assert all(qwords.count(n) == 1 for n in q.names)
    assert {p.order for p in ioi} == {"ABBA", "BABA"}
