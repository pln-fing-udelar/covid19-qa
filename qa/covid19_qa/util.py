# -*- coding: utf-8 -*-
from typing import Iterator, Sequence, TypeVar

T = TypeVar("T")


def chunks(seq: Sequence[T], n: int) -> Iterator[Sequence[T]]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(seq), n):
        yield seq[i:i + n]
