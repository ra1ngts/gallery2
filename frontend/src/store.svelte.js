// stateCtx
export const stateCtx = $state({
    artworks: [],
    categories: [],
    page: 'main',
    pages: {
        main: 'main',
        category: 'category',
        contact: 'contact',
        loading: 'loading'
    },
    menu: [
        {id: 'main', title: 'Main'},
        {id: 'category', title: 'Category'},
        {id: 'contact', title: 'Contact'}
    ]
});