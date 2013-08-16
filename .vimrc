syntax on
set number
set ruler
set hlsearch
set expandtab
set tabstop=2
set shiftwidth=2
set autoindent
set smartindent
set cindent
set noswapfile
set modeline
set ls=2

highlight OverLength ctermbg=red ctermfg=white guibg=#592929
match OverLength /\%81v.\+/

let &t_Co=256

let mapleader = ","

inoremap jk <Esc>

colorscheme jellybeans
filetype on

" vimrc
nnoremap <leader>ev :w<CR>:edit $MYVIMRC<CR>
nnoremap <leader>sv :source $MYVIMRC<CR>

" window
nnoremap <leader>wv :vsplit<CR>
nnoremap <leader>ws :split<CR>
nnoremap <leader>wl <C-W>l
nnoremap <leader>wh <C-W>h
nnoremap <leader>wj <C-W>j
nnoremap <leader>wk <C-W>k
nnoremap <leader>ww <C-W>w
nnoremap <leader>] gt
nnoremap <leader>[ gT
nnoremap <space> :noh<CR>

" buffer
nnoremap <leader>b :bp<CR>
nnoremap <leader>ss :wa<CR>

"command p
let g:ctrlp_map = ';'
let g:ctrlp_custom_ignore = { 'dir':  '\v[\/]\.(git|hg|svn)$', 'file': '\v\.(class)' }

execute pathogen#infect()

autocmd Filetype java set tags=.tags
autocmd Filetype java set omnifunc=javacomplete#Complete
autocmd Filetype java set completefunc=javacomplete#CompleteParamsInfo

inoremap <leader>c <C-X><C-O>
inoremap <leader>x <C-X><C-U>
