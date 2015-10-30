
all: wavetable_data.h

wavetable_data.h: wavetable.py
	rm -f wavetable.data
	python wavetable.py
	(printf "const " & xxd -i wavetable.data) | cat > wavetable_data.h
	rm wavetable.data
