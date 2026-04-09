// stateCtx
export const stateCtx = $state({
    artworks: [],
    menu: [
        {id: 'main', title: 'Main'},
        {id: 'category', title: 'Category'},
        {id: 'about', title: 'About'},
        {id: 'contact', title: 'Contact'}
    ],
    activeMenu: 'main'
});

// export const contactForm = (recaptcha_token = null) => {
//   const form = new FormData();
//   form.set('name', stateCtx.contactsData.name || '');
//   form.set('subject', stateCtx.contactsData.subject || '');
//   form.set('message', stateCtx.contactsData.message || '');
//   form.set('email', stateCtx.contactsData.email || '');

//   if (recaptcha_token) {
//     form.set('recaptcha_token', recaptcha_token);
//   }

//   console.log('contactForm has sent data:', Object.fromEntries(form.entries()));
//   return form;
// };