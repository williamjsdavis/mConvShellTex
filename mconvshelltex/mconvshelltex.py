import pickle

#import xarray as _xr
import numpy as _np

import matplotlib.tri as _tri
import matplotlib.cm as _cm
import matplotlib.animation as _an
import matplotlib.pyplot as _plt

"""Load various pickle data"""
def load_pkl(filename):
    with open(filename, "rb") as input_file:
        d_out = pickle.load(input_file)
    return d_out

"""Load xy grid data"""
def load_xygrid():
    filename = "mConvShellTex/mconvshelltex/xygrid.pkl"
    return load_pkl(filename)

"""Load radius data"""
def load_radius():
    filename = "mConvShellTex/mconvshelltex/radius.pkl"
    return load_pkl(filename)

"""Load example temperature data"""
def load_example_tdata():
    filename = "mConvShellTex/mconvshelltex/tdata-example.pkl"
    return load_pkl(filename)

## Colormaps

"""Make scaled colormap"""
def make_cmap(rmin,rmax,cmapName='hot'):
    cmap_interp = lambda r: _np.interp(r,[rmin,rmax],[0,1])

    # Named colormap
    c_set = _cm.get_cmap(cmapName)
    c_set_map = lambda r: _np.array(c_set(cmap_interp(r))).reshape(-1,4)
    return c_set_map

## Animation functions

"""Plot single contours, variable angle"""
def single_frame_viewangle(ax,fieldData,iv_radius,c_set_map,elev,azim):
  ax.clear()
  for (i_radius,v_radius) in iv_radius[::ri_step]:
    if any(fieldData > p_levels[0]):
      ax.tricontourf(
          triang,
          fieldData,
          p_levels,
          zdir='z',
          colors=c_set_map(v_radius),
          offset=v_radius
      )
  ax.set_zlim(
      (min(data.r),
      max(data.r))
  )
  ax.set_box_aspect((5, 3, 1), zoom=1.2)
  ax.set_axis_off()
  ax.view_init(elev=elev, azim=azim)
  return ax

"""Rotate the viewing angle"""
def animate_rotate(ax,fieldData,iv_radius,c_set_map,i):
  elev = 30
  azim = _np.interp(i,[0,200],[-65,295])
  ax = single_frame_viewangle(ax,fieldData,iv_radius,c_set_map,elev,azim)
  return ax

"""First animation function for single contour level"""
def make_animation(filename,dpi=80,fps=25,level=2425,ri_step=50):
    # Figure object + 3D projection
    fig = _plt.figure(
        dpi=dpi
    )
    ax = fig.add_subplot(111,projection='3d')

    # Single contour level
    p_levels = [level,10000]

    # Decimating radius levels for speed (default ri_step=50)
    radius = load_radius()
    iv_radius = [(i_radius,v_radius) for (i_radius,v_radius) in enumerate(radius)]

    # Loading data
    tdata = load_example_tdata()
    fieldData = tdata["tdata"].flatten()

    # Colormap
    rmin = float(fieldData.max())
    rmax = float(fieldData.max())
    c_set_map = make_cmap(rmin,rmax,cmapName='hot')

    # Make animation handle
    anim_handle = lambda i: animate_rotate(ax,fieldData,iv_radius,c_set_map,i)

    # Make animation 
    ani = _an.FuncAnimation(fig, animate_rotate, interval=40, repeat=True, frames=180)
    ani.save(filename, dpi=dpi, writer=_an.PillowWriter(fps=fps))
