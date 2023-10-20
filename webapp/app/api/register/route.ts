export async function POST(request: Request) {
    return new Promise(r => setTimeout(r, 3000,
        new Response("Зареєстровано успішно", {
            status: 200,
        })));

    // return new Promise(r => setTimeout(r, 3000,
    //     new Response("Не зареєстровано, повторіть спробу", {
    //         status: 500,
    //     })));
};
