import { createClient } from '@/utils/supabase/server';
import { cookies } from 'next/headers';

export default async function Page() {
    const cookieStore = await cookies();
    const supabase = createClient(cookieStore);

    try {
      const { data: products } = await supabase.from('Product').select('id, analyzed');
      console.log(products);

      return (
        <ul>
          {products?.map((product) => (
            <li key={product.id}>{product.id} - {product.analyzed ? 'Analyzed' : 'Not Analyzed'}</li>
          ))}
        </ul>
      );
    } catch (error) {
      console.error('Error fetching products:', error);
      return <p>Error fetching products.</p>;
    }
}