from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class ITitles(ABC):
    title: str | None = None
    subtitle: str | None = None
    x: str | None = None
    y: str | None = None
    z: str | None = None

    @staticmethod
    def write_html(
        text: str, color="navy", size: float = 12, shape: str = "DejaVu Sans"
    ) -> str:
        """Write a text in HTML."""
        out = f"<span style='color: {color}; font-size: {size}px; font-family: {shape}'>{text}</span>"
        return out

    def write_main(self) -> str | None:
        if self.title is not None:
            out = self.title
            if self.subtitle is not None:
                out = out + "<br>" + self.subtitle
        return out

    @abstractmethod
    def write_title(self, *args):
        """Write the title."""
        pass

    @abstractmethod
    def write_subtitle(self, *args):
        """Write the subtitle."""
        pass
