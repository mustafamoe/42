import abc
import typing


NumericData = int | float | list[int | float]
TextData = str | list[str]
LogEntry = dict[str, str]
LogData = LogEntry | list[LogEntry]


class DataProcessor(abc.ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self._items: list[tuple[int, str]] = []
        self._next_rank = 0

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        raise NotImplementedError

    def output(self) -> tuple[int, str]:
        if len(self._items) == 0:
            raise IndexError("No processed data available")
        return self._items.pop(0)

    def total_processed(self) -> int:
        return self._next_rank

    def remaining_count(self) -> int:
        return len(self._items)

    def _store(self, value: str) -> None:
        self._items.append((self._next_rank, value))
        self._next_rank += 1


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Numeric Processor")

    def validate(self, data: typing.Any) -> bool:
        if self._is_number(data):
            return True
        if not isinstance(data, list):
            return False
        return all(self._is_number(item) for item in data)

    def ingest(self, data: NumericData) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for value in data:
                self._store(str(value))
        else:
            self._store(str(data))

    def _is_number(self, data: typing.Any) -> bool:
        return type(data) in (int, float)


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Text Processor")

    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, str):
            return True
        if not isinstance(data, list):
            return False
        return all(isinstance(item, str) for item in data)

    def ingest(self, data: TextData) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for value in data:
                self._store(value)
        else:
            self._store(data)


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Log Processor")

    def validate(self, data: typing.Any) -> bool:
        if self._is_log_entry(data):
            return True
        if not isinstance(data, list):
            return False
        return all(self._is_log_entry(item) for item in data)

    def ingest(self, data: LogData) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, list):
            for entry in data:
                self._store(self._format_log_entry(entry))
        else:
            self._store(self._format_log_entry(data))

    def _is_log_entry(self, data: typing.Any) -> bool:
        if not isinstance(data, dict):
            return False
        return all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in data.items()
        )

    def _format_log_entry(self, entry: LogEntry) -> str:
        if "log_level" in entry and "log_message" in entry:
            return f"{entry['log_level']}: {entry['log_message']}"
        return ", ".join(
            f"{key}: {value}" for key, value in entry.items()
        )


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for element in stream:
            if not self._process_element(element):
                print(
                    "DataStream error - Can't process element in stream: "
                    f"{element}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if len(self._processors) == 0:
            print("No processor found, no data")
            return
        for processor in self._processors:
            total = processor.total_processed()
            remaining = processor.remaining_count()
            print(
                f"{processor.name}: total {total} items processed, "
                f"remaining {remaining} on processor"
            )

    def _process_element(self, element: typing.Any) -> bool:
        for processor in self._processors:
            if processor.validate(element):
                try:
                    processor.ingest(element)
                except Exception as error:
                    print(f"DataStream error - {error}")
                return True
        return False


def consume_outputs(processor: DataProcessor, count: int) -> None:
    for _ in range(count):
        try:
            processor.output()
        except IndexError:
            return


def main() -> None:
    stream = DataStream()
    numeric_processor = NumericProcessor()
    text_processor = TextProcessor()
    log_processor = LogProcessor()
    batch: list[typing.Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected",
            },
        ],
        42,
        ["Hi", "five"],
    ]

    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...")
    stream.print_processors_stats()

    print("Registering Numeric Processor")
    stream.register_processor(numeric_processor)
    print(f"Send first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("Registering other data processors")
    stream.register_processor(text_processor)
    stream.register_processor(log_processor)
    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print(
        "Consume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
    )
    consume_outputs(numeric_processor, 3)
    consume_outputs(text_processor, 2)
    consume_outputs(log_processor, 1)
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
