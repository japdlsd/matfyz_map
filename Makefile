
src/initial_full_list.txt: src/bak.html src/mag.html parseList.py
	rm -f src/initial_full_list.txt
	python3 parseList.py src/bak.html > src/initial_full_list.txt
	python3 parseList.py src/mag.html >> src/initial_full_list.txt
	python3 erase_copies.py src/initial_full_list.txt

src/bak.html:
	./get_raw_lists.sh

src/mag.html:
	./get_raw_lists.sh

src/mat.txt:
	rm -f src/mat.txt
	python3 parseList.py src/sp_MAT.html > src/mat.txt
	python3 parseList.py src/sp_mMAT.html >> src/mat.txt
	python3 erase_copies.py src/mat.txt