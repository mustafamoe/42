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


class ExportPlugin(typing.Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        values = [
            self._format_field(value) for _, value in data
        ]
        print("CSV Output:")
        print(",".join(values))

    def _format_field(self, value: str) -> str:
        if self._needs_quotes(value):
            return f'"{value.replace("\"", "\"\"")}"'
        return value

    def _needs_quotes(self, value: str) -> bool:
        return (
            "," in value
            or '"' in value
            or "\n" in value
            or "\r" in value
        )


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        values = [
            f'"item_{rank}": "{self._escape_json(value)}"'
            for rank, value in data
        ]
        print("JSON Output:")
        print("{" + ", ".join(values) + "}")

    def _escape_json(self, value: str) -> str:
        result = ""
        for char in value:
            result += self._escape_json_char(char)
        return result

    def _escape_json_char(self, char: str) -> str:
        if char == "\\":
            return "\\\\"
        if char == '"':
            return '\\"'
        if char == "\b":
            return "\\b"
        if char == "\f":
            return "\\f"
        if char == "\n":
            return "\\n"
        if char == "\r":
            return "\\r"
        if char == "\t":
            return "\\t"
        if ord(char) < 32:
            return "\\u" + format(ord(char), "04x")
        return char


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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        if nb <= 0:
            return
        for processor in self._processors:
            data = self._consume_processor(processor, nb)
            if len(data) > 0:
                plugin.process_output(data)

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

    def _consume_processor(
        self,
        processor: DataProcessor,
        count: int,
    ) -> list[tuple[int, str]]:
        data: list[tuple[int, str]] = []
        for _ in range(count):
            try:
                data.append(processor.output())
            except IndexError:
                return data
        return data


def build_first_batch() -> list[typing.Any]:
    return [
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


def build_second_batch() -> list[typing.Any]:
    return [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {
                "log_level": "ERROR",
                "log_message": "500 server crash",
            },
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]


def main() -> None:
    stream = DataStream()
    csv_plugin = CSVExportPlugin()
    json_plugin = JSONExportPlugin()
    first_batch = build_first_batch()
    second_batch = build_second_batch()

    print("=== Code Nexus - Data Pipeline ===")
    print("Initialize Data Stream...")
    stream.print_processors_stats()

    print("Registering Processors")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    print(f"Send first batch of data on stream: {first_batch}")
    stream.process_stream(first_batch)
    stream.print_processors_stats()

    print("Send 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, csv_plugin)
    stream.print_processors_stats()

    print(f"Send another batch of data: {second_batch}")
    stream.process_stream(second_batch)
    stream.print_processors_stats()

    print("Send 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, json_plugin)
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
