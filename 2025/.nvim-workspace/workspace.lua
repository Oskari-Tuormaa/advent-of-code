local nmap = require("config.utils").nmap

nmap("<leader>e", "<cmd>sp term://cmake --build build -j<cr>")
nmap("<leader>bp", "<cmd>sp term://cmake --fresh -B build -G Ninja<cr>")

nmap("<leader>E", function()
    vim.notify("Here we go")
    local days = vim.fn.glob("day*", true, true)
    local cmd = "sp term://cmake --build build -j"

    for _, k in pairs(days) do
        cmd = cmd .. " && echo && build/" .. k ..'/'.. k
    end

    vim.cmd(cmd)
end)

nmap("<leader>W", function()
    local day_idx = vim.fn.input({
        prompt="Day to watch"
    })
    local day = string.format("day%02d", day_idx)
    local execute_cmd = "build/".. day .."/".. day

    vim.cmd([[ belowright vs term://bash -c 'fd \| entr -cs \"cmake --build build -j && ]].. execute_cmd ..[[\"' ]])
end)
