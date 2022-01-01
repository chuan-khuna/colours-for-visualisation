import numpy as np


def to_array(array_like):
    return np.round(np.array(array_like, dtype=np.float), 2)


def to_list(array_like, r=2):
    return np.round(array_like, r).tolist()


def to_list_int(array_like):
    return np.array(array_like, dtype=np.int)


class Theme:
    """[summary]
    calculate size in point unit for using in matplotlib theme
    """

    def __init__(self, figsize=(10, 5), dpi=200, n_elem=200, n_base_font=25, font_step=1.618):
        """[summary]
        n_elem: number of row of element (dot) in vertical axis
        n_base_font: number of row of base font in vertical axis
        """

        assert isinstance(figsize, (tuple, list, np.ndarray))
        assert isinstance(dpi, int)
        assert dpi > 0
        assert isinstance(n_elem, int)
        assert n_elem > 0
        assert isinstance(n_base_font, int)
        assert n_base_font > 0
        assert isinstance(font_step, float)
        assert font_step > 0

        # point per inch
        # 1 point = 1/72 inch
        self.PPI = 72

        self.dpi = dpi
        self.figsize = to_array(figsize)
        self.n_elem = n_elem
        self.n_base_font = n_base_font
        self.font_step = font_step

        self._update()

        self.theme = self._get_theme()

        pass

    def _update(self):
        # calculate things
        self.aspect_ratio = np.round(self.figsize / np.min(self.figsize), 2)
        self.figsize_px = self.figsize * self.dpi
        self.figsize_pt = self.figsize * self.PPI
        self.px_per_pt = np.round(self.dpi / np.float(self.PPI), 2)
        self.element_pt = np.round(self._inch_per_elem(self.figsize[1], self.n_elem) * self.PPI, 2)
        self.base_font_pt = np.round(self._inch_per_elem(self.figsize[1], self.n_base_font) * self.PPI, 2)

    def _get_theme(self):
        self._update()
        return {
            'figsize_inch': to_list(self.figsize),
            'aspect_ratio': to_list(self.aspect_ratio),
            'dpi': self.dpi,
            'pixel_per_point': self.px_per_pt,
            'figsize_px': to_list_int(self.figsize_px),
            'figsize_pt': to_list(self.figsize_pt),
            'vertical_element_pt': self.element_pt,
            'vertical_base_font_pt': self.base_font_pt,
            'font_sizes': self.get_font_sizes(1, 1)
        }

    def _inch_per_elem(self, inch, n_elem):
        return np.round(inch / n_elem, 2)

    def _how(self):
        self._update()
        print(f"""\
1 point = 1/72 inch
PPI: point per inch = 72
---
inch -> point = inch * PPI
point -> px = (1/PPI) * DPI
aspect ratio(w:h) = {self.aspect_ratio[0]} : {self.aspect_ratio[1]}
""")

    def set_dpi(self, dpi):
        assert isinstance(dpi, int)
        assert dpi > 0

        self.dpi = dpi
        self._update()

    def set_figsize(self, figsize):
        assert isinstance(figsize, (tuple, list, np.ndarray))
        self.figsize = figsize
        self._update()

    def set_n_elem(self, n_elem):
        assert isinstance(n_elem, int)
        assert n_elem > 0

        self.n_elem = n_elem
        self._update()

    def n_base_font(self, n_base_font):
        assert isinstance(n_base_font, int)
        assert n_base_font > 0

        self.n_base_font = n_base_font
        self._update()

    def set_font_step(self, font_step):
        assert isinstance(font_step, float)
        assert font_step > 0

        self.font_step = font_step
        self._update()

    def get_font_sizes(self, n_lower=2, n_higher=2):
        assert n_lower > 0 and n_higher > 0
        assert isinstance(n_lower, int) and isinstance(n_higher, int)
        x = np.round(self.font_step**np.arange(-n_lower, n_higher + 1, 1), 2)
        return to_list(x * self.base_font_pt, 1)
