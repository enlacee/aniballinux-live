#include "mouse_highlight.h"
#include <QColor>
#include <QPainter>
#include <kwin/effects.h>

namespace KWin {

MouseHighlightEffect::MouseHighlightEffect() {}

MouseHighlightEffect::~MouseHighlightEffect() = default;

bool MouseHighlightEffect::isActive() const { return true; }

void MouseHighlightEffect::paintScreen(int mask, const QRegion &region,
                                       ScreenPaintData &data) {
  effects->paintScreen(mask, region, data);

  QPointF cursorPos = effects->cursorPos();

  // En KWin 6, el rendering puede ser complejo, pero para un ejemplo pro:
  // QPainter sobre el actual renderTarget es la forma más "legible"
  QPainter painter(effects->renderTarget());
  painter.setRenderHint(QPainter::Antialiasing);

  QColor color(255, 0, 0, 180);
  painter.setPen(QPen(Qt::white, 2));
  painter.setBrush(color);

  int radius = 20;
  painter.drawEllipse(cursorPos, radius, radius);
}

} // namespace KWin

#include "mouse_highlight.moc"
K_EXPORT_KWIN_EFFECT(mousehighlight, KWin::MouseHighlightEffect)
