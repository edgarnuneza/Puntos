function verificar(form){
	contraseña1 = form.password.value;
	contraseña2 = form.password_confirmar.value;
	
	if(contraseña1 != contraseña2){

		return false;
	}
	else{
		return true;
	}
}