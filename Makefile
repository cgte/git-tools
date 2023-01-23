system_install:
	 which cargo || curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
install:
	cargo install just
	just install

test:
	just test
