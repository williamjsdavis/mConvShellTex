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

class SceneSingleLevel():
    
    """Construct base scene properties"""
    def __init__(self,level=2425,ri_step=50,dpi=80):
        # Figure object + 3D projection
        self.fig = _plt.figure(
            dpi=dpi
        )
        self.ax = self.fig.add_subplot(111,projection='3d')

        # Single contour level
        self.p_levels = [level,10000]

        # Triangular mesh
        self.triang = self.gen_mesh()

        # Decimating radius levels for speed (default ri_step=50)
        self.ri_step = ri_step
        self.radius = load_radius()
        self.r_min = min(self.radius)
        self.r_max = max(self.radius)
        self.iv_radius = [(i_radius,v_radius) for (i_radius,v_radius) in enumerate(self.radius)]

        # Loading example field data
        tdata = load_example_tdata()
        self.exampleFieldData = tdata["tdata"].flatten()

        # Colormap
        self.c_set_map = make_cmap(self.r_min,self.r_max,cmapName='hot')

    """Generate triangulated mesh"""
    def gen_mesh(self):
        xygrid = load_xygrid()
        xgrid = xygrid["xgrid"].flatten()
        ygrid = xygrid["ygrid"].flatten()
        return _tri.Triangulation(xgrid, ygrid)

    """Plot single contours, variable angle"""
    def single_frame_viewangle(self,fieldData,elev,azim):
        #self.ax.clear()
        for (i_radius,v_radius) in self.iv_radius[::self.ri_step]:
            if any(fieldData > self.p_levels[0]):
                self.ax.tricontourf(
                    self.triang,
                    fieldData,
                    self.p_levels,
                    zdir='z',
                    colors=self.c_set_map(v_radius),
                    offset=v_radius
                )
        self.ax.set_zlim((
            self.r_min,
            self.r_max)
        )
        self.ax.set_box_aspect((5, 3, 1), zoom=1.2)
        #self.ax.set_axis_off()
        self.ax.view_init(elev=elev, azim=azim)
        return None

    """Rotate the viewing angle"""
    def animate_rotate(self,fieldData,i):
        elev = 30
        azim = _np.interp(i,[0,200],[-65,295])
        self.single_frame_viewangle(fieldData,elev,azim)
        return None

    """First animation function for single contour level"""
    def make_stationary_animation(self,filename,dpi=80,fps=25):
        
        # Make animation handle
        anim_handle = lambda i: self.animate_rotate(self.exampleFieldData,i)

        # Make animation 
        ani = _an.FuncAnimation(fig, anim_handle, interval=40, repeat=True, frames=180)
        ani.save(filename, dpi=dpi, writer=_an.PillowWriter(fps=fps))
