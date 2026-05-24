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


def test_numeric_processor() -> None:
    processor = NumericProcessor()

    print("Testing Numeric Processor...")
    print(f"Trying to validate input '42': {processor.validate(42)}")
    print(f"Trying to validate input 'Hello': {processor.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    invalid_numeric: typing.Any = "foo"
    try:
        processor.ingest(invalid_numeric)
    except Exception as error:
        print(f"Got exception: {error}")

    data: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {data}")
    processor.ingest(data)

    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = processor.output()
        print(f"Numeric value {rank}: {value}")


def test_text_processor() -> None:
    processor = TextProcessor()

    print("Testing Text Processor...")
    print(f"Trying to validate input '42': {processor.validate(42)}")

    data = ["Hello", "Nexus", "World"]
    print(f"Processing data: {data}")
    processor.ingest(data)

    print("Extracting 1 value...")
    rank, value = processor.output()
    print(f"Text value {rank}: {value}")


def test_log_processor() -> None:
    processor = LogProcessor()
    data = [
        {
            "log_level": "NOTICE",
            "log_message": "Connection to server",
        },
        {
            "log_level": "ERROR",
            "log_message": "Unauthorized access!!",
        },
    ]

    print("Testing Log Processor...")
    print(f"Trying to validate input 'Hello': {processor.validate('Hello')}")
    print(f"Processing data: {data}")
    processor.ingest(data)

    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = processor.output()
        print(f"Log entry {rank}: {value}")


def main() -> None:
    print("=== Code Nexus - Data Processor ===")
    test_numeric_processor()
    test_text_processor()
    test_log_processor()


if __name__ == "__main__":
    main()
