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
```

## Gotchas

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
