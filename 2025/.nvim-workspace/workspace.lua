local nmap = require("config.utils").nmap

nmap("<leader>e", "<cmd>sp term://cmake --build build<cr>")
nmap("<leader>E", "<cmd>sp term://cmake --build build; ./build/day01/day01<cr>")
nmap("<leader>bp", "<cmd>sp term://cmake -B build<cr>")
