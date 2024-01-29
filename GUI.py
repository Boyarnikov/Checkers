import flet as ft

from flet import Theme


class CellFabric:
    @staticmethod
    def generate_cell(x, y):
        #button = ft.FilledButton(
        #    text=str(x + y * 8),
        #    style=ft.ButtonStyle(
        #        shape=ft.RoundedRectangleBorder(radius=0),
        #        overlay_color=ft.colors.TRANSPARENT
        #    )
        #)

        cell = ft.Container(
            content=ft.Text(x + y * 8),
            alignment=ft.alignment.center,
            width=50,
            height=50,
            bgcolor=ft.colors.PRIMARY if (x + y) % 2 else ft.colors.SECONDARY_CONTAINER
        )

        return cell


def main(page: ft.Page):
    page.title = "checkers"

    page.theme = Theme(color_scheme_seed='green')
    board = ft.Column(
        [
            ft.Row(
                [
                    CellFabric.generate_cell(j, i) for j in range(8)
                ],
                spacing=0,
            ) for i in range(8)
        ],
        spacing=0,
    )

    page.add(
        board
    )

    page.update()


ft.app(target=main)
