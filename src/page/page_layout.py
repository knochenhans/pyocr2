from typing import List, Optional

from loguru import logger

from src.page.ocr_box import OCRBox


class PageLayout:
    def __init__(self, boxes: List[OCRBox]) -> None:
        self.boxes: List[OCRBox] = boxes
        self.region: tuple = (0, 0, 0, 0)  # (x, y, width, height)
        self.header_y: int = 0
        self.footer_y: int = 0

    def get_page_region(self) -> tuple:
        return (
            self.region[0],
            self.header_y,
            self.region[2],
            self.region[3] - self.header_y - self.footer_y,
        )

    def sort_boxes(self) -> None:
        self.boxes.sort(key=lambda box: box.order)
        self.update_order()

    def update_order(self) -> None:
        for index, box in enumerate(self.boxes):
            box.order = index

    def move_box(self, index: int, new_index: int) -> None:
        box_to_move = self.boxes.pop(index)
        self.boxes.insert(new_index, box_to_move)
        self.update_order()

    def remove_box(self, index: int) -> None:
        self.boxes.pop(index)
        self.update_order()

    def add_box(self, box: OCRBox, index: Optional[int] = None) -> None:
        if index is None:
            self.boxes.append(box)
        else:
            self.boxes.insert(index, box)
        self.update_order()

    def get_box(self, index: int) -> OCRBox:
        return self.boxes[index]
    
    def replace_box(self, index: int, box: OCRBox) -> None:
        self.boxes[index] = box

    def __len__(self) -> int:
        return len(self.boxes)

    def __iter__(self):
        return iter(self.boxes)

    def __getitem__(self, index: int) -> OCRBox:
        return self.boxes[index]

    def __setitem__(self, index: int, box: OCRBox) -> None:
        self.boxes[index] = box

    def __delitem__(self, index: int) -> None:
        self.boxes.pop(index)

    def __str__(self) -> str:
        return f"PageLayout(boxes={self.boxes})"

    def __repr__(self) -> str:
        return self.__str__()