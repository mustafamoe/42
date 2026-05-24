# Python Module 05 Notes

## Big idea

This module is about polymorphism.

The main goal is to define one shared processor interface, implement different
processor classes, and route mixed data through the same workflow.

Authorized imports from the subject:

- `abc`
- `typing`

## Key concepts

`ABC` creates an abstract base class.

`@abstractmethod` marks methods that child classes must override.

Method overriding means a child class provides its own version of a method from
the parent class.

Polymorphism lets `DataStream` call `validate()` and `ingest()` on any
`DataProcessor` without knowing the exact processor type.

`Protocol` describes a duck-typed interface. A class is compatible when it has
the required method, even if it does not inherit from the protocol.

## Exercise 0: Data Processor

File: `ex0/data_processor.py`

Subject requirements:

- Directory: `ex0/`
- File to submit: `data_processor.py`
- Authorized: builtins, standard types, `import typing`, `import abc`
- Not allowed: any imports except `typing` and `abc`
- Create abstract class `DataProcessor` inheriting from `ABC`.
- Define abstract `validate(self, data: Any) -> bool`.
- Define abstract `ingest(self, data: Any) -> None`.
- Define shared `output(self) -> tuple[int, str]`.
- `output()` returns and removes the oldest stored item plus its processor-local
  rank.
- `NumericProcessor` accepts `int`, `float`, and mixed lists of both.
- `TextProcessor` accepts `str` and lists of strings.
- `LogProcessor` accepts `dict[str, str]` and lists of that type.
- Each concrete `ingest()` signature must reflect the data accepted by that
  processor.
- Invalid data passed directly to `ingest()` must raise an exception.
- Tests must show valid and invalid `validate()` calls, one invalid direct
  `ingest()` call, ingestion, and `output()`.

Idea:

Create `DataProcessor` as an abstract class, then implement:

- `NumericProcessor`
- `TextProcessor`
- `LogProcessor`

Each processor validates input, ingests supported data, stores processed string
items, and returns the oldest stored item with `output()`.

Useful pattern:

```python
rank, value = processor.output()
```

Important lesson:

All processors share the same public interface, but each class validates and
formats its own data type.

## Exercise 1: Data Stream

File: `ex1/data_stream.py`

Subject requirements:

- Directory: `ex1/`
- File to submit: `data_stream.py`
- Authorized: builtins, standard types, `import typing`, `import abc`
- Not allowed: any imports except `typing` and `abc`
- Reuse and improve Exercise 0 code.
- Create `DataStream`.
- Implement `register_processor(self, proc: DataProcessor) -> None`.
- Implement `process_stream(self, stream: list[typing.Any]) -> None`.
- Route each stream element to an appropriate registered processor through
  `validate()`/`ingest()` polymorphism.
- Print an error when no processor can handle an element.
- Implement `print_processors_stats(self) -> None`.
- Test stream processing, statistics, consuming outputs, and updated
  statistics.

Idea:

Create `DataStream` to register processors and route every element of a mixed
list to the first processor that validates it.

Useful methods:

- `register_processor(proc)`
- `process_stream(stream)`
- `print_processors_stats()`

Important lesson:

`DataStream` depends on the `DataProcessor` interface, not on concrete processor
details. This makes adding a new processor easier.

## Exercise 2: Data Pipeline

File: `ex2/data_pipeline.py`

Subject requirements:

- Directory: `ex2/`
- File to submit: `data_pipeline.py`
- Authorized: builtins, standard types, `import typing`, `import abc`
- Not allowed: any imports except `typing` and `abc`
- Reuse and improve Exercise 1 code.
- Create `ExportPlugin` inheriting from `typing.Protocol`.
- Define `process_output(self, data: list[tuple[int, str]]) -> None` in the
  protocol.
- Add `output_pipeline(self, nb: int, plugin: ExportPlugin) -> None` to
  `DataStream`.
- `output_pipeline()` consumes up to `nb` elements from all registered data
  processors and sends them to the provided plugin.
- Create at least one CSV export plugin and one JSON export plugin.
- Manually create valid CSV and JSON strings.
- Not allowed: CSV/JSON helper imports or any other specific plugin imports.

Idea:

Add an output pipeline that consumes processed data from every registered
processor and sends it to an export plugin.

Plugins implemented:

- `CSVExportPlugin`
- `JSONExportPlugin`

Important lesson:

`ExportPlugin` is a `Protocol`. The pipeline only needs an object with a
compatible `process_output()` method.

## Commands

```text
python3 projects/python05/ex0/data_processor.py
python3 projects/python05/ex1/data_stream.py
python3 projects/python05/ex2/data_pipeline.py
python3 -m py_compile projects/python05/ex0/data_processor.py
python3 -m py_compile projects/python05/ex1/data_stream.py
python3 -m py_compile projects/python05/ex2/data_pipeline.py
python3.10 -m flake8 projects/python05
python3.10 -m mypy projects/python05
```

## Gotchas

The official subject is stored as `en.subject.pdf`, with extracted text in
`en.subject.txt`.

`output()` removes the oldest stored item.

The rank returned by `output()` is the item processing rank inside that
processor, so it does not reset when earlier items are consumed.

Lists are ingested item by item, not as one combined object.

CSV and JSON output are built manually because the subject does not authorize
extra imports.

## Module summary

```text
ex0: abstract processor classes and method overriding
ex1: stream routing through polymorphic processors
ex2: output plugins through protocol-based duck typing
```

Short version:

This module teaches how one shared interface can support many specialized
behaviors.
