
dtw.so: setup.py dtw.pyx
	python setup.py build_ext --inplace
	mv dtw.so ../dtw.so

.PHONY: clean
clean:
	rm -rf build cDTW*egg-info
