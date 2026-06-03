from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, RichLog
from textual.containers import Vertical, Container
from textual.color import Color
import asyncio

class BannerAnimado(Container):
    """Un widget de banner que cambia de color automáticamente."""
    def on_mount(self) -> None:
        # Animamos el color de fondo de azul a rojo continuamente
        self.animate("styles.background", Color.parse("#900c3f"), duration=2.0, easing="in_out_cubic")
        # Ciclo infinito de cambio de color cada 2 segundos
        self.set_interval(2.0, self.toggle_color)

    def toggle_color(self) -> None:
        target = "#1a5276" if self.styles.background == Color.parse("#900c3f") else "#900c3f"
        self.animate("styles.background", Color.parse(target), duration=2.0)

class MiAppTUI(App):
    CSS = """
    BannerAnimado {
        dock: top;
        height: 3;
        content-align: center middle;
        color: white;
        text-style: bold;
        border: double white;
    }
    #main_area {
        height: 1fr;
        border: solid green;
    }
    Input {
        dock: bottom;
    }
    """

    def compose(self) -> ComposeResult:
        yield BannerAnimado("SISTEMA ACTIVO - ESPERANDO ENTRADA")
        with Vertical(id="main_area"):
            yield RichLog(id="log", highlight=True, markup=True)
        yield Input(placeholder="Escribe algo y presiona Enter...")
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        log = self.query_one("#log", RichLog)
        texto = event.value.strip()
        
        if texto:
            log.write(f"[yellow]Procesando:[/] {texto}...")
            # Simulamos una carga pesada sin bloquear la animación del banner
            await asyncio.sleep(1.5)
            log.write(f"[green]Completado:[/] Se recibió '{texto}' con éxito.")
            event.input.value = ""  # Limpiar input
def main():
    MiAppTUI().run()

if __name__ == "__main__":
    main()