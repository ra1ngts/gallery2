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
        about: 'about',
        contact: 'contact',
        loading: 'loading'
    },
    menu: [
        {id: 'main', title: 'Main'},
        {id: 'category', title: 'Category'},
        {id: 'about', title: 'About'},
        {id: 'contact', title: 'Contact'}
    ]
});