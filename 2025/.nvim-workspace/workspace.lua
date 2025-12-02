local nmap = require("config.utils").nmap

nmap("<leader>e", "<cmd>sp term://cmake --build build<cr>")
nmap("<leader>bp", "<cmd>sp term://cmake -B build<cr>")

nmap("<leader>E", function()
    vim.notify("Here we go")
    local days = vim.fn.glob("day*", true, true)
    local cmd = "sp term://cmake --build build"

    for _, k in pairs(days) do
        cmd = cmd .. " && echo && build/" .. k ..'/'.. k
    end

    vim.cmd(cmd)
end)
