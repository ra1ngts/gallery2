// stateCtx
export const stateCtx = $state({
    artworks: [],
    categories: [],
    page: '',
    pages: {
        loading: 'loading',
        main: 'main',
        category: 'category',
        contact: 'contact'
    },
    menu: {
        main: 'Main',
        category: 'Category',
    }
});