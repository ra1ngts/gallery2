// stateCtx
export const stateCtx = $state({
    profile: {},
    artworks: [],
    artworksCategory: [],
    featuredWork: {},
    categories: [],
    page: 'main',
    categorySlug: null,
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