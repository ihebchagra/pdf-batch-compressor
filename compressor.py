#!/usr/bin/env python3
import subprocess
import os
import sys
import shutil

def compress(input_file_path, output_file_path):
	# Basic controls
	# Check if valid path
	if not os.path.isfile(input_file_path):
	    print("Error: invalid path for input PDF file")
	    sys.exit(1)

	# Check if file is a PDF by extension
	if input_file_path.split('.')[-1].lower() != 'pdf':
	    print("Error: input file is not a PDF")
	    sys.exit(1)

	gs = get_ghostscript_path()
	print("Compress PDF...")
	initial_size = os.path.getsize(input_file_path)
	subprocess.call([gs, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
	                '-dPDFSETTINGS=/screen',
	                '-dNOPAUSE', '-dQUIET', '-dBATCH',
	                '-sOutputFile={}'.format(output_file_path),
	                 input_file_path]
	)
	final_size = os.path.getsize(output_file_path)
	ratio = 1 - (final_size / initial_size)
	print("Compression by {0:.0%}.".format(ratio))
	print("Final file size is {0:.1f}MB".format(final_size / 1000000))
	print("Done.")


def get_ghostscript_path():
	gs_names = ['gs', 'gswin32', 'gswin64']
	for name in gs_names:
	    if shutil.which(name):
	        return shutil.which(name)
	raise FileNotFoundError(f'No GhostScript executable was found on path ({"/".join(gs_names)})')


def main():
	try:
		os.mkdir("compressed")
	except:
		pass
	indir='pdfs'
	outdir='compressed'
	for filename in os.listdir(indir):
		print("Compressing", filename)
		infile = os.path.join(indir, filename)
		outfile = os.path.join(outdir, filename)
		compress(infile, outfile)


if __name__ == '__main__':
	main()
