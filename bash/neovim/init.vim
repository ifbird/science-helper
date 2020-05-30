" ----- Variables -----------------------------------------------------

" For python virtual environment, you should assign one
" virtualenv for Neovim, then install pynvim for it,
" then hard-code the interpreter path. So that the "pynvim" package
" is not required for each virtualenv.
" Use expand to make ~ correctly expanded.
let g:python3_host_prog = expand('~/opt/anaconda3/bin/python')

" Custom mapping <leader> (see `:h mapleader` for more info)
" The default is '\'
" let mapleader = ','

" Main configurations
" use :echo g:is_linux to check the values
let g:is_win = has('win32') || has('win64')
let g:is_linux = has('unix') && !has('macunix')
let g:is_mac = has('macunix')




" ----- vim-plug -----------------------------------------------------
"
" Install vim-plug for Neovim:
" Put plug.vim in ~/.local/share/nvim/site/autoload
" $ curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
"   https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
"
" Install plugins: :PlugInstall
" Update plugins : :PlugUpdate
" Remove plugins : :PlugClean (First, comment the plugin install command in
"                  init.vim. Open Nvim and use :PlugClean to uninstall plugins)
" Check the plugin status: :PlugStatus
" Upgrade vim-plug itself: :PlugUpgrade
"
" Disable a plugin: Plug 'foo/bar', { 'on': [] }
"
" reference: https://jdhao.github.io/2018/12/24/centos_nvim_install_use_guide_en/

" ----- Begin
call plug#begin('~/.config/nvim/plugged')

" ----- deoplete: dark powered neo-completion, auto-completion plugin designed for
" Neovim/Vim8
Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }

" ----- deoplete-jedi

" Install pynvim for a conda environment:
" $ conda install -c conda-forge pynvim

" Install jedi for a conda environment:
" $ conda install jedi

" Install msgpack 1.0.0
" $ conda install -c conda-forge msgpack-python

" Add plugin
Plug 'zchee/deoplete-jedi'

" ----- vim-airline: fancy status bar
Plug 'vim-airline/vim-airline'

" ----- vim-airline-themes: change the vim-airline themes

" In order to correctly show the airline statusbar, you need to install
" powerline fonts
" $ sudo apt-get install fonts-powerline

" Add patched fonts for powerline
" $ git clone https://github.com/powerline/fonts.git --depth=1
" $ fonts/install.sh
" $ rm -rf fonts

" Select proper fonts for the terminal

" Add plugin
Plug 'vim-airline/vim-airline-themes'

" check symbols
" :help airline-customization

" choose a default theme
" :AirlineTheme <theme>: change theme
let g:airline_theme='papercolor'

" ----- auto-pairs: automatic quote and bracket completion
" Plug 'jiangmiao/auto-pairs'

" ----- nerdcommenter
" <leader>cc: comment the line
" <leader>cu: uncomment the line
" <leader>: \ as default
Plug 'scrooloose/nerdcommenter'

" ----- neoformat

" Install yapf to work together with neoformat to format python
" $ conda install -c conda-forge yapf

" Add plugin
" Plug 'sbdchd/neoformat'


" ----- vim-autoformat
" Use these command to manually format
" format all: :Autoformat
" autoindent: gg=G
" retab: :retab
" remove trailing whitespace: :RemoveTrailingSpaces

" Add plugin
Plug 'Chiel92/vim-autoformat'


" ----- jedi-vim
Plug 'davidhalter/jedi-vim'

" ----- nerdtree
" NERDTreeToggle: toggle nerdtree
" o: open file in a new buffer or open/close dir
" t: open file in a new tab
" i: open file in a new horizontal split, -
" s: open file in a new vertical split, |
" u: go to parent dir
" r: refresh current dir
" q: close nerdtree window
Plug 'scrooloose/nerdtree', { 'on':  'NERDTreeToggle' }

" ----- vim-rainbow
Plug 'luochen1990/rainbow'

" ----- rainbow_parentheses
Plug 'junegunn/rainbow_parentheses.vim'

" ----- vim-highlightedyank: highlight the yanked text
Plug 'machakann/vim-highlightedyank'

" ----- SimplyFold: fold the code
Plug 'tmhedberg/SimpylFold', { 'on': [] }

" ----- vim-signify: Show git change (change, delete, add) signs in vim sign column
Plug 'mhinz/vim-signify'
" Another similar plugin
" Plug 'airblade/vim-gitgutter'

" ----- vim-fugitive: Git command inside vim
Plug 'tpope/vim-fugitive', {'on': ['Gstatus']}

" ----- gv.vim: Git commit browser
" Turn on fugitive by :Gstatus, then you can use :GV
Plug 'junegunn/gv.vim', { 'on': 'GV' }

" ----- A list of colorscheme plugin you may want to try. Find what suits you.
Plug 'morhetz/gruvbox'  " gruvbox
Plug 'lifepillar/vim-gruvbox8'  " gruvbox8, gruvbox8_hard, gruvbox8_soft
Plug 'srcery-colors/srcery-vim'  " srcery
Plug 'joshdick/onedark.vim'  " onedark
Plug 'iCyMind/NeoSolarized'  " NeoSolarized
Plug 'sickill/vim-monokai'  "monokai
Plug 'NLKNguyen/papercolor-theme'  " PaperColor
Plug 'sjl/badwolf'  " badwolf
Plug 'ajmwagar/vim-deus'  " deus
Plug 'YorickPeterse/happy_hacking.vim'  " happy_hacking
Plug 'lifepillar/vim-solarized8'  " solarized8, solarized8_flat, solarized8_high, solarized8_low
Plug 'whatyouhide/vim-gotham'  " gotham, gotham256
Plug 'rakr/vim-one'  " one
Plug 'kaicataldo/material.vim'  " material

" ----- End of vim-plug
call plug#end()




" ----- Plugin Configurations ------------------------------------------------


" ----- deoplete settings

" Wheter to enable deoplete automatically after start nvim
let g:deoplete#enable_at_startup = 1

" Maximum candidate window width
call deoplete#custom#source('_', 'max_menu_width', 80)

" Minimum character length needed to activate auto-completion.
call deoplete#custom#source('_', 'min_pattern_length', 1)

" Whether to disable completion for certain syntax
" call deoplete#custom#source('_', {
"     \ 'filetype': ['vim'],
"     \ 'disabled_syntaxes': ['String']
"     \ })
call deoplete#custom#source('_', {
      \ 'filetype': ['python'],
      \ 'disabled_syntaxes': ['Comment']
      \ })

" Ignore certain sources, because they only cause nosie most of the time
" This will cause the <tab> complete not working well
" call deoplete#custom#option('ignore_sources', {
"       \ '_': ['around', 'buffer', 'tag']
"       \ })

" Candidate list item number limit
call deoplete#custom#option('max_list', 30)

" The number of processes used for the deoplete parallel feature.
call deoplete#custom#option('num_processes', 16)

" The delay for completion after input, measured in milliseconds.
call deoplete#custom#option('auto_complete_delay', 100)

" Enable deoplete auto-completion
call deoplete#custom#option('auto_complete', v:true)

" Automatically close function preview windows after completion
" see https://github.com/Shougo/deoplete.nvim/issues/115.
autocmd InsertLeave,CompleteDone * if pumvisible() == 0 | pclose | endif

" Tab-complete, see https://vi.stackexchange.com/q/19675/15292.
inoremap <expr><TAB> pumvisible() ? "\<C-n>" : "\<TAB>"


" ----- deoplete-jedi settings

" Whether to show doc string
let g:deoplete#sources#jedi#show_docstring = 0

" For large package, set autocomplete wait time longer
let g:deoplete#sources#jedi#server_timeout = 50

" Ignore jedi errors during completion
let g:deoplete#sources#jedi#ignore_errors = 1


" ----- jedi-vim settings

" Disable autocompletion, because I use deoplete for auto-completion
let g:jedi#completions_enabled = 0

" Whether to show function call signature
let g:jedi#show_call_signatures = '0'


" ----- nerdtree settigns

" Map nerdtree toggle to F2,
" here CR> is carriage return, equal to CTRL-M
map <F2> :NERDTreeToggle<CR>

" Delete a file buffer when you have deleted it in nerdtree
let NERDTreeAutoDeleteBuffer = 1

" Show current root as realtive path from HOME in status bar,
" see https://github.com/scrooloose/nerdtree/issues/891
let NERDTreeStatusline="%{exists('b:NERDTree')?fnamemodify(b:NERDTree.root.path.str(), ':~'):''}"

" Disable bookmark and 'press ? for help' text
let NERDTreeMinimalUI=0

" Set NERDTree window size
let g:NERDTreeWinSize=30


" ----- vim-rainbow

" set to 0 if you want to enable it later via :RainbowToggle
let g:rainbow_active = 0


" ----- rainbow_parentheses
" RainbowParentheses
au bufenter * RainbowParentheses


" ----- vim-autoformat
" Remap the command of autoformat to <F3>
noremap <F3> :Autoformat<CR>

" Make do endo indent correct
let fortran_do_enddo=1


" ----- vim-airline settings
" utils functions: https://gist.github.com/jdhao/b1828028edf4ef41188ca42a7e29fd3f
" Set airline theme to a random one if it exists
" let s:candidate_airlinetheme = ['ayu_mirage', 'base16_flat',
"     \ 'base16_grayscale', 'lucius', 'hybridline', 'ayu_dark',
"     \ 'base16_adwaita', 'biogoo', 'distinguished', 'jellybeans',
"     \ 'luna', 'raven', 'term', 'vice', 'zenburn']
" let s:idx = utils#RandInt(0, len(s:candidate_airlinetheme)-1)
" let s:theme = s:candidate_airlinetheme[s:idx]

" if utils#HasAirlinetheme(s:theme)
"     let g:airline_theme=s:theme
" endif

" Tabline settings
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#formatter = 'unique_tail_improved'

" Show buffer number for easier switching between buffer,
" see https://github.com/vim-airline/vim-airline/issues/1149
let g:airline#extensions#tabline#buffer_nr_show = 1

" Buffer number display format
let g:airline#extensions#tabline#buffer_nr_format = '%s. '

" Whether to show function or other tags on status line
let g:airline#extensions#tagbar#enabled = 1

" Skip empty sections if there are nothing to show,
" extracted from https://vi.stackexchange.com/a/9637/15292
let g:airline_skip_empty_sections = 1

" Whether to use powerline symbols, see https://vi.stackexchange.com/q/3359/15292
let g:airline_powerline_fonts = 1

if !exists('g:airline_symbols')
  let g:airline_symbols = {}
endif
let g:airline_symbols.branch = '⎇'
" let g:airline_symbols.paste = 'ρ'
let g:airline_symbols.spell = 'Ꞩ'

" Only show git hunks which are non-zero
let g:airline#extensions#hunks#non_zero_only = 1

" Speed up airline
let g:airline_highlighting_cache = 1


" ----- vim-highlightedyank

" this fixes the issue for some colorschemes
hi HighlightedyankRegion cterm=reverse gui=reverse

" set highlight duration time to 1000 ms, i.e., 1 second
let g:highlightedyank_highlight_duration = 1000


" ----- vim-signify settings
" The VCS to use
let g:signify_vcs_list = [ 'git' ]

" Change the sign for certain operations
let g:signify_sign_change = '~'

" default updatetime 4000ms is not good for async update
set updatetime=100

" ----- neoformat

" Enable alignment
" let g:neoformat_basic_format_align = 1

" Enable tab to spaces conversion
" let g:neoformat_basic_format_retab = 1

" Enable trimmming of trailing whitespace
" let g:neoformat_basic_format_trim = 1




" ----- Options -----------------------------------------------------
" reference: https://github.com/jdhao/nvim-config/blob/master/options.vim
" use :verbose set <name> to check detailed configurations of <name>

" line numbers
set number

" Paste mode toggle, it seems that Neovim's bracketed paste mode
" does not work very well for nvim-qt, so we use good-old paste mode
set pastetoggle=<F12>

" Split window below/right when creating horizontal/vertical windows
set splitbelow splitright

" Clipboard settings, always use clipboard for all delete, yank, change, put
" operation, see https://stackoverflow.com/q/30691466/6064933
set clipboard+=unnamedplus

" General tab settings
set tabstop=2       " number of visual spaces per TAB
set softtabstop=2   " number of spaces in tab when editing
set shiftwidth=2    " number of spaces to use for autoindent
set expandtab       " expand tab to spaces so that tabs are spaces
" These will be reset to 4 in /usr/share/nvim/runtime/ftplugin/python.vim
" if g:python_recommended_style does not exist or non-zero
let g:python_recommended_style = 0

" Set matching pairs of characters and highlight matching brackets
" Use % to jump between them
set matchpairs+=<:>

" Ignore case in general, but become case-sensitive when uppercase is present
set ignorecase smartcase

" File and script encoding settings for vim
set fileencoding=utf-8
set fileencodings=ucs-bom,utf-8,cp936,gb18030,big5,euc-jp,euc-kr,latin1
scriptencoding utf-8

" Break line at predefined characters
set linebreak
" Character to show before the lines that have been soft-wrapped
set showbreak=↪

" Show current line where the cursor is
set cursorline
" Set a ruler at column 80, see https://stackoverflow.com/q/2447109/6064933
set colorcolumn=80

" Minimum lines to keep above and below cursor when scrolling.
" This will make some context visible around where you are working.
set scrolloff=3

" Use mouse to put cursor, select and resize windows, etc.
set mouse=nc  " Enable mouse in several mode
set mousemodel=popup  " Set the behaviour of mouse

" Do not show mode on command line since vim-airline can show it
set noshowmode

" Fileformats to use for new files, determining the EOL
set fileformats=unix,dos

" The way to show the result of substitution in real time for preview
" nosplit: do not open a new split window
" split: show the results in a new split window
set inccommand=nosplit

" Ask for confirmation when handling unsaved or read-only files
set confirm

" Do not use visual and errorbells
set visualbell noerrorbells

" The level we start to fold
set foldlevel=0

" The number of command and search history to keep
set history=500

" Use list mode and customized listchars
set list listchars=tab:▸\ ,extends:❯,precedes:❮,nbsp:+

" Auto-write the file based on some condition
set autowrite

" Show hostname, full path of file and last-mod time on the window title. The
" meaning of the format str for strftime can be found in
" http://man7.org/linux/man-pages/man3/strftime.3.html. The function to get
" lastmod time is drawn from https://stackoverflow.com/q/8426736/6064933
set title
set titlestring=
if g:is_linux
  set titlestring+=%(%{hostname()}\ \ %)
endif
set titlestring+=%(%{expand('%:p:~')}\ \ %)
set titlestring+=%{strftime('%Y-%m-%d\ %H:%M',getftime(expand('%')))}

" Persistent undo even after you close a file and re-open it
set undofile

" Do not show "match xx of xx" and other messages during auto-completion
set shortmess+=c

" Completion behaviour
" set completeopt+=noinsert  " Auto select the first completion entry
set completeopt+=menuone  " Show menu even if there is only one item
set completeopt-=preview  " Disable the preview window

" Settings for popup menu
set pumheight=15  " Maximum number of items to show in popup menu

" Scan files given by `dictionary` option
" if has('unix')
"   set dictionary+=/usr/share/dict/words
" else
"   set dictionary+=~/AppData/Local/nvim/words
" endif
" Use <c-n> and <c-p> instead of <c-x><c-k> to complete
" This does not work now, I do not know why.
" set complete+=kspell complete-=w complete-=b complete-=u complete-=t
" set spelllang=en,cjk  " Spell languages
" set spellsuggest+=10  " The number of suggestions shown in the screen for z=

" Align indent to next multiple value of shiftwidth. For its meaning,
" see http://vim.1045645.n5.nabble.com/shiftround-option-td5712100.html
set shiftround

" Virtual edit is useful for visual block edit
" It makes you enable to select a rectangle visual block
set virtualedit=block

" Correctly break multi-byte characters such as CJK,
" see https://stackoverflow.com/q/32669814/6064933
set formatoptions+=mM

" Disable automatic comment insertion
" https://vi.stackexchange.com/questions/1983/how-can-i-get-vim-to-stop-putting-comments-in-front-of-new-lines
au FileType * set fo-=c fo-=r fo-=o

" Tilde (~) is an operator, thus must be followed by motions like `e` or `w`.
set tildeop

" Do not add two spaces after a period when joining lines or formatting texts,
" see https://stackoverflow.com/q/4760428/6064933
set nojoinspaces

" Text after this column number is not highlighted
set synmaxcol=500

" Go to other lines without changing the column
set nostartofline

" Search visullay selected part by typing '//'                                  
vnoremap // y/\V<C-r>=escape(@",'/\')<CR><CR> 




" ----- Auto Commands -----------------------------------------------------

" ----- Do not use smart case in command line mode, extracted from https://vi.stackexchange.com/a/16511/15292.
augroup dynamic_smartcase
  autocmd!
  autocmd CmdLineEnter : set nosmartcase
  autocmd CmdLineLeave : set smartcase
augroup END

augroup term_settings
  autocmd!
  " Do not use number and relative number for terminal inside nvim
  autocmd TermOpen * setlocal norelativenumber nonumber
  " Go to insert mode by default to start typing command
  autocmd TermOpen * startinsert
augroup END

" ----- More accurate syntax highlighting? (see `:h syn-sync`)
augroup accurate_syn_highlight
  autocmd!
  autocmd BufEnter * :syntax sync fromstart
augroup END

" ----- Return to last edit position when opening a file
augroup resume_edit_position
  autocmd!
  autocmd BufReadPost *
        \ if line("'\"") > 1 && line("'\"") <= line("$") && &ft !~# 'commit'
        \ | execute "normal! g`\"zvzz"
        \ | endif
augroup END

" ----- Display a message when the current file is not in utf-8 format.
" Note that we need to use `unsilent` command here because of this issue:
" https://github.com/vim/vim/issues/4379
augroup non_utf8_file_warn
  autocmd!
  autocmd BufRead * if &fileencoding != 'utf-8'
        \ | unsilent echomsg 'File not in UTF-8 format!' | endif
augroup END




" ----- Mappings -----------------------------------------------------

" Toggle search highlight, see https://stackoverflow.com/a/26504944/6064933
nnoremap <silent><expr> <F4> (&hls && v:hlsearch ? ':nohls' : ':set hls')."\n"

" Move the cursor based on physical lines, not the actual lines.
nnoremap <silent> <expr> j (v:count == 0 ? 'gj' : 'j')
nnoremap <silent> <expr> k (v:count == 0 ? 'gk' : 'k')
nnoremap <silent> ^ g^
nnoremap <silent> 0 g0

" When completion menu is shown, use <cr> to select an item and do not add an
" annoying newline. Otherwise, <enter> is what it is. For more info , see
" https://superuser.com/a/941082/736190 and
" https://unix.stackexchange.com/q/162528/221410
inoremap <expr> <cr> ((pumvisible())?("\<C-Y>"):("\<cr>"))
" Use <esc> to close auto-completion menu
" inoremap <expr> <esc> ((pumvisible())?("\<C-e>"):("\<esc>"))




" ----- UI -----------------------------------------------------


" ----- General settings about colors
" Enable true colors support. Do not set this option if your terminal does not
" support true colors! For a comprehensive list of terminals supporting true
" colors, see https://github.com/termstandard/colors and
" https://gist.github.com/XVilka/8346728.
if $TERM == "xterm-256color" || exists('g:started_by_firenvim')
  set termguicolors
endif
" Use dark background
set background=dark


" ----- Colorscheme settings

""""" Set the background to transparent after every colorscheme command
au ColorScheme * hi Normal ctermbg=none guibg=none
" au ColorScheme myspecialcolors hi Normal ctermbg=red guibg=red

""""" gruvbox settings
" We should check if theme exists before using it, otherwise you will get
" error message when starting Nvim
" if utils#HasColorscheme('gruvbox8')
"   " Italic options should be put before colorscheme setting,
"   " see https://github.com/morhetz/gruvbox/wiki/Terminal-specific#1-italics-is-disabled
"   let g:gruvbox_italics=1
"   let g:gruvbox_italicize_strings=1
"   let g:gruvbox_filetype_hi_groups = 0
"   let g:gruvbox_plugin_hi_groups = 0
"   colorscheme gruvbox8_hard
" else
"   colorscheme desert
" endif
" Italic options should be put before colorscheme setting,
" see https://github.com/morhetz/gruvbox/wiki/Terminal-specific#1-italics-is-disabled
let g:gruvbox_italics=1
let g:gruvbox_italicize_strings=1
let g:gruvbox_filetype_hi_groups = 0
let g:gruvbox_plugin_hi_groups = 0
colorscheme gruvbox8_hard

""""" deus settings
" colorscheme deus

""""" solarized8 settings
" Solarized colorscheme without bullshit
" let g:solarized_term_italics=1
" let g:solarized_visibility="high"
" colorscheme solarized8_high

""""" vim-one settings
" let g:one_allow_italics = 1
" colorscheme one

""""" material.vim settings
" let g:material_terminal_italics = 1
" " theme_style can be 'default', 'dark' or 'palenight'
" let g:material_theme_style = 'dark'
" colorscheme material

""""" badwolf settings
" let g:badwolf_darkgutter = 0
" " Make the tab line lighter than the background.
" let g:badwolf_tabline = 2
" colorscheme badwolf


" ----- Cursor colors and shapes
" highlight groups for cursor color
highlight Cursor cterm=bold gui=bold guibg=cyan guifg=black
highlight Cursor2 guifg=red guibg=red

" Set up cursor color and shape in various mode, ref:
" https://github.com/neovim/neovim/wiki/FAQ#how-to-change-cursor-color-in-the-terminal
" set guicursor=n-v-c:block-Cursor/lCursor,i-ci-ve:ver25-Cursor2/lCursor2,r-cr:hor20,o:hor20
" set guicursor=n-v-c:block-Cursor/lCursor,i-ci-ve:block-Cursor2/lCursor2,r-cr:hor20,o:hor20
set guicursor=  " use guicursor from the colorscheme




" ----- Others -----------------------------------------------------

" The terminal supports 24-bit/truecolor if the colors blend smoothly
" $ awk 'BEGIN{
"     s="/\\/\\/\\/\\/\\"; s=s s s s s s s s;
"     for (colnum = 0; colnum<77; colnum++) {
"         r = 255-(colnum*255/76);
"         g = (colnum*510/76);
"         b = (colnum*255/76);
"         if (g>255) g = 510-g;
"         printf "\033[48;2;%d;%d;%dm", r,g,b;
"         printf "\033[38;2;%d;%d;%dm", 255-r,255-g,255-b;
"         printf "%s\033[0m", substr(s,colnum+1,1);
"     }
"     printf "\n";
" }'

" The terminal supports 24-bit/truecolor if the text displays in red
" $ printf "\x1b[38;2;255;100;0mTRUECOLOR\x1b[0m\n"
