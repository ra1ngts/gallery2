import { stateCtx } from './store.svelte';

export const getCategory = async (slug) => {
    try {
      stateCtx.page = stateCtx.pages.loading;

      const response = await fetch(`/${slug}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      if (data.status === 'success') {
        stateCtx.page = stateCtx.pages.category;
        stateCtx.artworksCategory = data.artworks;
        stateCtx.categoryTitle = data.title;
        window.scrollTo({ top: 0, behavior: 'instant' });
        console.log('category (POST) successfully sending:', data);
      } else {
        stateCtx.page = stateCtx.pages.main;
        console.error('category (POST) sending error:', data);
      }
    } catch (error) {
      console.error('Error in getCategory has been caught:', error);
    }
};

export const routeChoice = (route) => {
    stateCtx.page = route.page;
    console.log(route.page);

    if (route.page === stateCtx.pages.category) {
      console.log('category route', route.page === stateCtx.pages.category);
      stateCtx.categorySlug = route.slug;
      console.log('category slug', route.slug);
      getCategory(route.slug);
    } else {
      stateCtx.categorySlug = null;
    }
};

// formateDate
export function formateDate(date) {
    if (!date) return '...';

    const dateObj = new Date(date);

    if (isNaN(dateObj.getTime())) {
        console.error(`Error date formatting: ${date}`);
        return 'Date not found';
    }

    return dateObj.toLocaleDateString('ru-RU', { month: '2-digit', year: 'numeric' }).replace('.', ' / ');
}

// getDuration
// export function getDuration(startDate, endDate, isCurrent) {
//     const start = formateDate(startDate);
    
//     if (isCurrent || !endDate) {
//         return `${start} — ${stateCtx.translation.utils?.present}`;
//     }
    
//     const end = formateDate(endDate);
//     return `${start} — ${end}`;
// }

// Email address validation
export function isEmailValidate(email) {
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    // console.log('isEmailValidate:', pattern.test(email));
    return pattern.test(email);
}

// Check touched field
export function markAsTouched(field) {
    stateCtx.touchedFields[field] = true;
    checkFields();
}

// checkFields
export function checkFields() {
    if (stateCtx.contactsData.name === '') {
        stateCtx.formErrors['name'] = ''; //stateCtx.translation.contact?.errors.name;
    } else {
        delete stateCtx.formErrors['name'];
    }

    if (!isEmailValidate(stateCtx.contactsData.email) || stateCtx.contactsData.email === '') {
        stateCtx.formErrors['email'] = ''; //stateCtx.translation.contact?.errors.email;
    } else {
        delete stateCtx.formErrors['email'];
    }

    if (stateCtx.contactsData.subject === '') {
        stateCtx.formErrors['subject'] = ''; //stateCtx.translation.contact?.errors.subject;
    } else {
        delete stateCtx.formErrors['subject'];
    }

    if (stateCtx.contactsData.message === '') {
        stateCtx.formErrors['message'] = ''; //stateCtx.translation.contact?.errors.message;
    } else {
        delete stateCtx.formErrors['message'];
    }
}

// showToast
export function showToast(message, type = 'success') {
    stateCtx.toast = { show: true, message, type };

    setTimeout(() => {
        stateCtx.toast.show = false;
    }, 3000);
}

// DATA = {
//     year: 2012,
//     month: 8,
//     day: 13
// }

// function getAge() {
//     const DATE = new Date();
//     const CURRENT_YEAR = DATE.getFullYear();
//     const CURRENT_MONTH = DATE.getMonth() + 1;
//     const CURRENT_DAY = DATE.getDate();

//     let age = CURRENT_YEAR - DATA.year;

//     if (CURRENT_MONTH < DATA.month || (CURRENT_MONTH === DATA.month && CURRENT_DAY < DATA.day)) {
//         age--;
//     }
//     console.log('age', age);
//     return age;
// }

// getAge();