# Data sources and download procedure

## 1. First build: LEVIR-CD
Official project/download page: https://justchenhao.github.io/LEVIR/
Official repository and terms: https://github.com/justchenhao/LEVIR
Original paper: https://levir.buaa.edu.cn/publications/remotesensing-798405-eng.pdf

Start with the original LEVIR-CD, not LEVIR-CD+. Follow the provider's download links, extract locally and preserve the supplied train/validation/test partitions. Arrange files as data/raw/levir_cd/{train,val,test}/{A,B,label}/filename.png. A is the first image, B the second, label the binary change mask; verify temporal ordering in the source documentation. Rename the validation directory to val if necessary. Matching names must exist in all three directories. Run scripts/validate_dataset.py.

The source describes 637 paired 1024x1024 RGB images at 0.5m/pixel in Texas. Labels include building growth AND decline: this is building change, not automatically new construction. Inspect each predicted region to assign direction, or add directional labels later. It is paired optical imagery, not itself multimodal data.

The provider restricts data to academic use and prohibits commercial use. Use for an academic learning experiment, cite the dataset, and seek clarification before use outside those terms. Do not bundle imagery in a public commercial demo; share code and only examples permitted by the terms.

Start by inspecting 10-20 training pairs. For a compute-limited pilot, select a reproducible subset from each existing partition; label all results as subset results. Keep all crops of one parent pair in one partition. For stronger geographic evaluation use the provider's supplemental location information to group by region, and report this separately from the official split.

## 2. Later UAE experiment: Sentinel-2 L2A
Browser: https://browser.dataspace.copernicus.eu/
Catalogue API: https://documentation.dataspace.copernicus.eu/APIs/STAC.html
Collection details: https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/S2L2A.html
Alternative catalogue: https://planetarycomputer.microsoft.com/docs/reference/stac/

Select a small UAE area, comparable seasons and low-cloud scenes at two dates. Record item IDs, acquisition dates, bounds, coordinate system, bands, pixel size, nodata and cloud-mask rules. Download only the area/bands needed through provider-supported access, respecting account and quota requirements.

Sentinel-2 RGB bands are 10m; SCL is 20m. Match coordinate reference system, bounds and pixel grid, resample continuous imagery appropriately and use nearest-neighbour for categorical cloud masks. Exclude clouds/shadows/nodata from BOTH metrics and the valid-area denominator. Do not treat upsampling as extra resolution.

This is a separate area-level change experiment. LEVIR's high-resolution RGB model cannot simply be assumed to work on 10m Sentinel imagery. You need local labels and evaluation; without them the UAE overlay is an exploratory visualization only. Do not claim building counts or construction detection accuracy.

## 3. Optional contextual data
OpenStreetMap exports and attribution: https://www.openstreetmap.org/copyright
Overpass documentation: https://wiki.openstreetmap.org/wiki/Overpass_API

Road/building context is an optional later multimodal branch. Check spatial and temporal alignment: current building polygons can reveal the answer when predicting historical changes. Use information available at the decision date. If trustworthy dated context is unavailable, defer fusion and document the limitation.

No data have been downloaded in this starter. Download availability and access requirements remain provider-controlled.
