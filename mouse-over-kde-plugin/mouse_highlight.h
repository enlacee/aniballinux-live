#pragma once

#include <kwin/effect.h>
#include <QObject>
#include <QPointF>

namespace KWin {

class MouseHighlightEffect : public Effect {
    Q_OBJECT
public:
    MouseHighlightEffect();
    ~MouseHighlightEffect() override;

    void paintScreen(int mask, const QRegion &region, ScreenPaintData &data) override;
    bool isActive() const override;

private:
    // En KWin 6, cursorHotspot() nos da la posición actual
};

} // namespace KWin
