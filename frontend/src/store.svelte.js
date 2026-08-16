// stateCtx
export const stateCtx = $state({
    profile: {},
    artworks: [],
    artworksCategory: [],
    featuredWork: {},
    categories: [],
    page: 'loading',
    categorySlug: null,
    pages: {
        main: 'main',
        category: 'category',
        about: 'about',
        contact: 'contact',
        loading: 'loading'
    },
    form: {},
    contactsData: {
        name: '',
        subject: '',
        message: '',
        email: ''
    },
    isSubmitting: false,
    formErrors: {},
    touchedFields: {},
    toast: {
        show: false,
        message: '',
        type: 'success'
    },
    activeSection: 'main',
    locale: 'en',
    translation: {}
});

export const contactForm = (recaptcha_token = null) => {
  const form = new FormData();
  form.set('name', stateCtx.contactsData.name || '');
  form.set('subject', stateCtx.contactsData.subject || '');
  form.set('message', stateCtx.contactsData.message || '');
  form.set('email', stateCtx.contactsData.email || '');

  if (recaptcha_token) {
    form.set('recaptcha_token', recaptcha_token);
  }

  console.log('contactForm has sent data:', Object.fromEntries(form.entries()));
  return form;
};