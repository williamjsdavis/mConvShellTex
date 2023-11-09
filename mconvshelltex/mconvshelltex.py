import os
import pickle
import urllib.request
import tarfile

import xarray as _xr
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

## Data accessing

data_index_lookup = [
    ("mantle01.tgz", (1,10), "edS6be3sk8oQ58N"),
    ("mantle02.tgz", (11,20), "infBBW2Rc9TJwf7"),
    ("mantle03.tgz", (21,30), "76Esj3yDP9EiaGc"),
    ("mantle04.tgz", (31,40), "AZmt47d48prCZZF"),
    ("mantle05.tgz", (41,50), "9fZ4A7ENGR6sQrc"),
    ("mantle06.tgz", (51,60), "B8HC3H4oqwcsWB3"),
    ("mantle07.tgz", (61,70), "t3zLJWWeirR5zmG"),
    ("mantle08.tgz", (71,80), "YmkYgxM7xxrNAwj"),
    ("mantle09.tgz", (81,90), "rMma6W9MBtQH9LX"),
    ("mantle10.tgz", (91,100), "MzcZBCaxaojTZJx"),
    ("mantle11.tgz", (101,110), "dfP6NXHmekQQrHR"),
    ("mantle12.tgz", (111,120), "2GnLRgPi8W2Dt5p"),
    ("mantle13.tgz", (121,130), "MqtoESg2d9DsF2P"),
    ("mantle14.tgz", (131,140), "ysGoJK6B3pLYaDB"),
    ("mantle15.tgz", (141,150), "Ae32XwCpt7bHo9D"),
    ("mantle16.tgz", (151,160), "AysWSPnxFS6e5B2"),
    ("mantle17.tgz", (161,170), "4NcnJkPYWpkXrmb"),
    ("mantle18.tgz", (171,180), "mBRfrnfEEEaKJ9m"),
    ("mantle19.tgz", (181,190), "J63KxeCppK8ssGc"),
    ("mantle20.tgz", (191,200), "NeqnHBNPWx4PRwd"),
    ("mantle21.tgz", (201,210), "JdzZQCKiHaRfL9L"),
    ("mantle22.tgz", (211,220), "DXnWtA5fymHBsxA"),
    ("mantle23.tgz", (221,230), "HzgtF42Pf9AnxGm"),
    ("mantle24.tgz", (231,240), "yy8FASeC8Dm54Sy"),
    ("mantle25.tgz", (241,251), "TC8QekmjokmBkWA"),
]

"""Use data index lookup to find tarfile name"""
def find_tarfile(i):
    if i < 1:
        ValueError("Out of bounds")
    for (name,indexRange,urlCode) in data_index_lookup:
        if (indexRange[0]<=i) & (i<=indexRange[1]):
            return name,urlCode
    raise ValueError("Out of bounds")

def request_tarfile(filenameTgz,outputFilename):
    urllib.request.urlretrieve(filenameTgz, filename=outputFilename)
    return None

"""Determine if the iteration count is at the start of a file section"""
def is_start(i):
    for (_,indexRange,_) in data_index_lookup:
        if (indexRange[0]==i):
            return True
    return False

"""Determine if the iteration count is at the end of a file section"""
def is_end(i):
    for (_,indexRange,_) in data_index_lookup:
        if (indexRange[1]==i):
            return True
    return False

"""Make the url for getting the tgz field files"""
def make_tgz_url(urlCode):
    return f"https://nextcloud.computecanada.ca/index.php/s/{urlCode}/download"


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
        tslice = tdata["tdata"].flatten()
        self.exampleFieldData = lambda i: tslice

        # Colormap
        self.c_set_map = make_cmap(self.r_min,self.r_max,cmapName='hot')

    """Requesting field data"""
    def load_field_data(self,i):
        # If the index is a start, request the tar file
        isStart = is_start(i)

        if isStart: 
            # Get filename and url code
            tarFile, urlCode = find_tarfile(i)

            # Make url
            urlTgz = make_tgz_url(urlCode)

            # Request file
            print(f"Downloading:{tarFile} @ {urlCode}")
            request_tarfile(urlTgz,tarFile)

            # Extract files from tar
            with tarfile.open(tarFile, "r:gz") as tar:
                tar.extractall()

            # Delete tar file
            print(f"Testing for file {tarFile}")
            if os.path.isfile(tarFile):
                print(f"Deleting file {tarFile}")
                os.remove(tarFile)

        # Load file from tar
        sphericalFile = f"spherical{i:03d}.nc"
        print(f"Loading:{sphericalFile}")

        # Load field data using xarray
        data = _xr.open_dataset(sphericalFile)

        # Delete .nc file
        print(f"Testing for file {sphericalFile}")
        if os.path.isfile(sphericalFile):
            print(f"Deleting file {sphericalFile}")
            os.remove(sphericalFile)
        
        return data.temperature.values

    """Generate triangulated mesh"""
    def gen_mesh(self):
        xygrid = load_xygrid()
        xgrid = xygrid["xgrid"].flatten()
        ygrid = xygrid["ygrid"].flatten()
        return _tri.Triangulation(xgrid, ygrid)

    """Plot single contours, variable angle"""
    def single_frame_viewangle(self,fieldData,elev,azim):
        self.ax.clear()
        for (i_radius,v_radius) in self.iv_radius[::self.ri_step]:
            fieldSlice = fieldData(i_radius)
            if any(fieldSlice > self.p_levels[0]):
                self.ax.tricontourf(
                    self.triang,
                    fieldSlice,
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
        self.ax.set_axis_off()
        self.ax.view_init(elev=elev, azim=azim)
        return None

    """Rotate the stationary scene"""
    def animate_rotate_stationary(self,fieldData,fullrotFrames,i):
        elev = 30
        azim = _np.interp(i,[0,fullrotFrames],[-65,295])
        self.single_frame_viewangle(fieldData,elev,azim)
        return None
    
    """Keep angle fixed"""
    def animate_fixed(self,i):
        print(f"frame: {i}")

        fieldData = self.load_field_data(i)
        fieldSlice = lambda i: fieldData[:,i,:].flatten()

        elev = 30
        azim = -65
        self.single_frame_viewangle(fieldSlice,elev,azim)
        return None

    """Keep angle fixed"""
    def animate_rotate(self,i,fullrotFrames):
        print(f"frame: {i}")

        fieldData = self.load_field_data(i)
        fieldSlice = lambda i: fieldData[:,i,:].flatten()

        elev = 30
        azim = _np.interp(i,[0,fullrotFrames],[-65,295])
        self.single_frame_viewangle(fieldSlice,elev,azim)
        return None

    """First animation function for single contour level"""
    def make_stationary_animation(self,filename,dpi=80,fps=25,frames=100,fullrotFrames=200):
        
        # Make animation handle
        anim_handle = lambda i: self.animate_rotate(self.exampleFieldData,fullrotFrames,i)

        # Make animation 
        ani = _an.FuncAnimation(
            self.fig, 
            anim_handle, 
            interval=40, 
            repeat=True, 
            frames=frames
        )
        ani.save(filename, dpi=dpi, writer=_an.PillowWriter(fps=fps))

    """Animation function for time-varying single contour level"""
    def make_vary_animation(self,filename,dpi=80,fps=25,frames=9):
        
        # Make animation handle
        anim_handle = lambda i: self.animate_fixed(i)

        # Make animation 
        ani = _an.FuncAnimation(
            self.fig, 
            anim_handle, 
            interval=40, 
            repeat=True, 
            frames=range(1,frames+1)
        )
        ani.save(filename, dpi=dpi, writer=_an.PillowWriter(fps=fps))

    """Animation function for time-varying, rotating single contour level"""
    def make_rotate_animation(self,filename,dpi=80,fps=25,frames=9,fullrotFrames=200):
        
        # Make animation handle
        anim_handle = lambda i: self.animate_rotate(i,fullrotFrames=fullrotFrames)

        # Make animation 
        ani = _an.FuncAnimation(
            self.fig, 
            anim_handle, 
            interval=40, 
            repeat=True, 
            frames=range(1,frames+1)
        )
        ani.save(filename, dpi=dpi, writer=_an.PillowWriter(fps=fps))
