# Colour Palette Analysis

- What are good palettes?
- Can I measure how good is it?
- How to ensure that my palette is safe for colour blind?
- Can I use AI generate an optimised colour palette?

- I try to figure out the keywords: `hue-saturation-brightness, contrast`. (distribution in someone's visualisation styles)

## How to choose `figsize=(w, h)`, `dpi`, `linewidth`, `markersize`

```py
# I mostly use seaborn

sns.lineplot(linewidth=...)
sns.scatterplot(s=...)
```

> To ask "How many element I want to show in a particular axis(length)?" might be easier to calculate the size of that element.

This may be a simple method to auto select element size that suite for a given figure size.

```py
# figsize = (w, h)
# PPI = 72, 1pt = 1/72 inch

elem_pt = (fig_h/n) * PPI
```

references:

- 1 typography point, 1 DTP point = 1/72 inch = 0.35mm
- [figsize's unit](https://matplotlib.org/stable/api/figure_api.html) is **inch**.
- [linewidth's unit](https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html) is **point**
- [matplotlib marker's `s`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.scatter.html#matplotlib.axes.Axes.scatter)
- `s = markersize ** 2`, markersize's unit is **point**
