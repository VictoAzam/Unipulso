"""
Módulo do Editor de Layout (WYSIWYG)
"""

from typing import Optional, Dict, Any
from PIL import Image, ImageTk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import colorchooser

from core import P_WIDTH, P_HEIGHT, NP_START_PX, PRINTABLE_W_PX
from core.models import TextItem, QRItem, LayoutModel
from core.render import render_layout_to_image
from utils import choose_font_file_for_family


class LayoutEditor:
    """Editor visual de layout (WYSIWYG) para pulseiras."""

    def __init__(self, root, layout: LayoutModel, fonts_map: Dict, logo_image: Optional[Image.Image] = None):
        self.root = root
        self.layout = layout
        self.fonts_map = fonts_map
        self.logo_image = logo_image
        self._dragging = {'id': None, 'offset': (0, 0)}
        self._prop_entries: Dict[str, Any] = {}

    def open(self, on_close_callback=None):
        """Abre a janela do editor."""
        win = tb.Toplevel(self.root)
        win.title('Editor de Layout')
        win.geometry('1000x500')

        # Painel esquerdo: Canvas (preview/edição)
        left = tb.Frame(win)
        left.pack(side=LEFT, fill=BOTH, expand=YES)
        self.editor_canvas = tb.Canvas(
            left,
            width=800,
            height=int(800 * (P_HEIGHT / P_WIDTH)),
            background='white'
        )
        self.editor_canvas.pack(fill=BOTH, expand=YES, padx=8, pady=8)

        # Painel direito: Propriedades
        right = tb.Labelframe(win, text='Propriedades do item')
        right.pack(side=RIGHT, fill=Y, padx=8, pady=8)

        # Combobox para escolher item
        tb.Label(right, text='Item:').pack(anchor='w')
        self.item_var = tb.StringVar()
        self.item_cb = tb.Combobox(
            right,
            textvariable=self.item_var,
            values=[it.get('id', '') for it in self.layout.items],
            width=25
        )
        self.item_cb.pack(fill=X, pady=4)

        def on_item_change(_evt=None):
            self._prop_load_from_selected()
            self._editor_render()

        self.item_cb.bind('<<ComboboxSelected>>', on_item_change)

        # Campos de propriedades
        def add_prop(label, key, default=''):
            frame = tb.Frame(right)
            frame.pack(fill=X, pady=2)
            tb.Label(frame, text=label, width=14).pack(side=LEFT)
            ent = tb.Entry(frame)
            ent.insert(0, str(default))
            ent.pack(side=RIGHT, fill=X, expand=YES)
            self._prop_entries[key] = ent

        add_prop('Tipo', 'type')
        add_prop('ID', 'id')
        add_prop('X', 'x')
        add_prop('Y', 'y')
        add_prop('Largura', 'width')
        add_prop('Rotação', 'rotation')
        add_prop('Texto', 'text')
        add_prop('Binding', 'binding')
        add_prop('Fonte', 'font_family')
        add_prop('Tamanho', 'font_size')
        add_prop('Negrito', 'bold')
        add_prop('Itálico', 'italic')
        add_prop('Cor', 'color')
        add_prop('Alinhamento', 'align')
        add_prop('Tamanho QR', 'size')
        add_prop('Data QR', 'data_text')

        # Controles avançados
        fam_frame = tb.Frame(right)
        fam_frame.pack(fill=X, pady=4)
        tb.Label(fam_frame, text='Fonte (lista)', width=14).pack(side=LEFT)
        families = sorted(self.fonts_map.keys())
        fam_cb2 = tb.Combobox(fam_frame, values=families, width=25)
        fam_cb2.pack(side=RIGHT, fill=X, expand=YES)
        self._prop_entries['font_family_cb'] = fam_cb2
        fam_cb2.bind('<<ComboboxSelected>>', lambda _e: self._prop_apply_changes())

        size_frame = tb.Frame(right)
        size_frame.pack(fill=X, pady=2)
        tb.Label(size_frame, text='Tam. (spin)', width=14).pack(side=LEFT)
        size_sb2 = tb.Spinbox(size_frame, from_=6, to=800, increment=1, width=8)
        size_sb2.pack(side=RIGHT)
        self._prop_entries['font_size_sb'] = size_sb2

        bi_frame = tb.Frame(right)
        bi_frame.pack(fill=X, pady=2)
        bold_var2 = tb.BooleanVar(value=False)
        italic_var2 = tb.BooleanVar(value=False)
        bold_cb2 = tb.Checkbutton(bi_frame, text='Negrito', variable=bold_var2)
        italic_cb2 = tb.Checkbutton(bi_frame, text='Itálico', variable=italic_var2)
        bold_cb2.pack(side=LEFT)
        italic_cb2.pack(side=LEFT)
        self._prop_entries['bold_var'] = bold_var2
        self._prop_entries['italic_var'] = italic_var2

        align_frame = tb.Frame(right)
        align_frame.pack(fill=X, pady=2)
        tb.Label(align_frame, text='Alinhamento', width=14).pack(side=LEFT)
        align_cb = tb.Combobox(align_frame, values=['left', 'center', 'right'], width=10)
        align_cb.pack(side=RIGHT)
        self._prop_entries['align_cb'] = align_cb
        align_cb.bind('<<ComboboxSelected>>', lambda _e: self._prop_apply_changes())

        color_frame = tb.Frame(right)
        color_frame.pack(fill=X, pady=2)
        tb.Label(color_frame, text='Cor (picker)', width=14).pack(side=LEFT)

        def pick_color():
            c = colorchooser.askcolor(title='Escolha a cor')
            if c and c[1]:
                ent = self._prop_entries.get('color')
                if ent:
                    ent.delete(0, 'end')
                    ent.insert(0, c[1])

        tb.Button(color_frame, text='Escolher...', command=pick_color).pack(side=RIGHT)

        btns = tb.Frame(right)
        btns.pack(fill=X, pady=6)
        tb.Button(btns, text='Aplicar', command=self._prop_apply_changes).pack(side=LEFT, padx=2)
        tb.Button(btns, text='Adicionar Texto', command=lambda: self._editor_add_item('text')).pack(side=LEFT, padx=2)
        tb.Button(btns, text='Adicionar QR', command=lambda: self._editor_add_item('qr')).pack(side=LEFT, padx=2)
        tb.Button(btns, text='Remover', command=self._editor_remove_selected).pack(side=LEFT, padx=2)

        # Interações de arrastar
        self.editor_canvas.bind('<Button-1>', self._on_canvas_click)
        self.editor_canvas.bind('<B1-Motion>', self._on_canvas_drag)
        self.editor_canvas.bind('<ButtonRelease-1>', self._on_canvas_release)

        # Inicializa
        if self.layout.items:
            self.item_var.set(self.layout.items[0].get('id', ''))
        self._editor_render()
        self._prop_load_from_selected()

        # Callback ao fechar
        if on_close_callback:
            win.protocol('WM_DELETE_WINDOW', lambda: (on_close_callback(), win.destroy()))

    def _scale_editor(self):
        cw = int(self.editor_canvas.winfo_width() or 800)
        ch = int(self.editor_canvas.winfo_height() or int(800 * (P_HEIGHT / P_WIDTH)))
        scale = min(cw / self.layout.width, ch / self.layout.height)
        return scale

    def _editor_render(self):
        self.editor_canvas.delete('all')
        scale = self._scale_editor()
        
        img = render_layout_to_image(self.layout, {}, self.fonts_map, logo_image=self.logo_image)
        disp = img.resize(
            (int(self.layout.width * scale), int(self.layout.height * scale)),
            Image.LANCZOS
        )
        self._editor_img = ImageTk.PhotoImage(disp)
        self.editor_canvas.create_image(0, 0, image=self._editor_img, anchor='nw', tags='bg')
        
        for it in self.layout.items:
            ix = int((it.get('x', 0)) * scale)
            iy = int((it.get('y', 0)) * scale)
            if it.get('type') == 'qr':
                s = int(it.get('size', 100) * scale)
                bbox = (ix, iy, ix + s, iy + s)
            else:
                w = int(it.get('width', 0) * scale) if it.get('width', 0) else int(200 * scale)
                bbox = (ix, iy, ix + w, iy + int(30 * scale))
            self.editor_canvas.create_rectangle(*bbox, outline='#007bff', dash=(3, 2), tags=('item', it.get('id', '')))

    def _find_item_by_id(self, _id: str) -> Optional[dict]:
        for it in self.layout.items:
            if it.get('id') == _id:
                return it
        return None

    def _selected_item_id(self) -> Optional[str]:
        return self.item_var.get() or None

    def _prop_load_from_selected(self):
        it = self._find_item_by_id(self._selected_item_id() or '')
        if not it:
            return
        
        for k, ent in self._prop_entries.items():
            try:
                if k == 'font_family_cb':
                    ent.set(str(it.get('font_family', '')))
                elif k == 'font_size_sb':
                    val = it.get('font_size', '')
                    ent.set(str(val))
                elif k == 'bold_var':
                    ent.set(bool(it.get('bold', False)))
                elif k == 'italic_var':
                    ent.set(bool(it.get('italic', False)))
                elif k == 'align_cb':
                    ent.set(str(it.get('align', 'left')))
                else:
                    ent.delete(0, 'end')
                    ent.insert(0, str(it.get(k, '')))
            except Exception:
                pass

    def _prop_apply_changes(self):
        it = self._find_item_by_id(self._selected_item_id() or '')
        if not it:
            return
        
        for k, ent in self._prop_entries.items():
            if k == 'font_family_cb':
                try:
                    it['font_family'] = ent.get()
                except Exception:
                    pass
                continue
            if k == 'font_size_sb':
                try:
                    it['font_size'] = int(ent.get())
                except Exception:
                    pass
                continue
            if k == 'bold_var':
                try:
                    it['bold'] = bool(ent.get())
                except Exception:
                    pass
                continue
            if k == 'italic_var':
                try:
                    it['italic'] = bool(ent.get())
                except Exception:
                    pass
                continue
            if k == 'align_cb':
                try:
                    it['align'] = ent.get()
                except Exception:
                    pass
                continue
            
            try:
                val = ent.get()
            except Exception:
                continue
            
            if k in ('x', 'y', 'width', 'font_size', 'size'):
                try:
                    it[k] = int(val)
                except Exception:
                    pass
            elif k in ('rotation',):
                try:
                    it[k] = float(val)
                except Exception:
                    pass
            elif k in ('bold', 'italic'):
                it[k] = str(val).strip().lower() in ('1', 'true', 'yes', 'on')
            else:
                it[k] = val
        
        self.item_cb['values'] = [it.get('id', '') for it in self.layout.items]
        self._editor_render()

    def _editor_add_item(self, t: str):
        new_id_base = 'item' if t == 'text' else 'qr'
        idx = 1
        ids = {it.get('id', '') for it in self.layout.items}
        while f'{new_id_base}{idx}' in ids:
            idx += 1
        
        if t == 'text':
            from dataclasses import asdict
            item = asdict(TextItem(id=f'{new_id_base}{idx}', x=NP_START_PX + 10, y=10, text='Novo Texto', font_size=24, align='left'))
        else:
            from dataclasses import asdict
            item = asdict(QRItem(id=f'{new_id_base}{idx}', x=NP_START_PX + 10, y=50, size=100, data_text='{Número da carteirinha}'))
        
        self.layout.items.append(item)
        self.item_cb['values'] = [it.get('id', '') for it in self.layout.items]
        self.item_var.set(item['id'])
        self._prop_load_from_selected()
        self._editor_render()

    def _editor_remove_selected(self):
        sid = self._selected_item_id()
        if not sid:
            return
        
        self.layout.items = [it for it in self.layout.items if it.get('id') != sid]
        vals = [it.get('id', '') for it in self.layout.items]
        self.item_cb['values'] = vals
        if vals:
            self.item_var.set(vals[0])
        else:
            self.item_var.set('')
        self._prop_load_from_selected()
        self._editor_render()

    def _canvas_to_model(self, x, y):
        scale = self._scale_editor()
        return int(x / scale), int(y / scale)

    def _on_canvas_click(self, evt):
        scale = self._scale_editor()
        clicked_id = None
        for it in reversed(self.layout.items):
            ix = int(it.get('x', 0) * scale)
            iy = int(it.get('y', 0) * scale)
            if it.get('type') == 'qr':
                s = int(it.get('size', 100) * scale)
                bbox = (ix, iy, ix + s, iy + s)
            else:
                w = int((it.get('width', 0) or 200) * scale)
                h = int(30 * scale)
                bbox = (ix, iy, ix + w, iy + h)
            
            if bbox[0] <= evt.x <= bbox[2] and bbox[1] <= evt.y <= bbox[3]:
                clicked_id = it.get('id')
                break
        
        if clicked_id:
            self.item_var.set(clicked_id)
            self._prop_load_from_selected()
            mx, my = self._canvas_to_model(evt.x, evt.y)
            it = self._find_item_by_id(clicked_id)
            self._dragging = {'id': clicked_id, 'offset': (mx - it.get('x', 0), my - it.get('y', 0))}
        else:
            self._dragging = {'id': None, 'offset': (0, 0)}

    def _on_canvas_drag(self, evt):
        if not self._dragging.get('id'):
            return
        mx, my = self._canvas_to_model(evt.x, evt.y)
        it = self._find_item_by_id(self._dragging['id'])
        if not it:
            return
        offx, offy = self._dragging['offset']
        it['x'] = max(0, mx - offx)
        it['y'] = max(0, my - offy)
        self._editor_render()

    def _on_canvas_release(self, _evt):
        if self._dragging.get('id'):
            self._prop_load_from_selected()
        self._dragging = {'id': None, 'offset': (0, 0)}
