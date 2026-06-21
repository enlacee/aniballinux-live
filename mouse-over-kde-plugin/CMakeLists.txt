cmake_minimum_required(VERSION 3.16)

project(mousehighlight)

# Encontrar dependencias básicas
find_package(ECM REQUIRED NO_MODULE)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH})

find_package(Qt6 REQUIRED COMPONENTS Core Gui Quick)
find_package(KF6 REQUIRED COMPONENTS Config CoreAddons WindowSystem)
find_package(KWin REQUIRED)

include(KDEInstallDirs)
include(KDECMakeSettings)
include(KDECompilerSettings NO_POLICY_SCOPE)

# El plugin
add_library(mousehighlight MODULE mouse_highlight.cpp)

target_link_libraries(mousehighlight
    Qt6::Core
    Qt6::Gui
    Qt6::Quick
    KF6::ConfigCore
    KF6::CoreAddons
    KF6::WindowSystem
    KWin::EffectBuiltins
)

# Esto genera el JSON embebido en la librería para KPlugin
kcoreaddons_desktop_to_json(mousehighlight metadata.json)

install(TARGETS mousehighlight DESTINATION ${KDE_INSTALL_PLUGINDIR}/kwin/effects)
